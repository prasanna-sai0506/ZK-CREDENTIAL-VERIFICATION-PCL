"""
Celery async task: OCR -> LLM -> ZK -> (optional) on-chain submit
"""

import logging
import uuid
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models.database import Job, OnChainProof, JobStatus
from app.models.schemas import ClaimSet
from app.services.ocr_service import extract_text_from_bytes
from app.services.llm_parser import extract_claims
from app.services.claim_validator import validate_and_normalise, build_bitmap
from app.services.zk_generator import generate_proof
from app.services.storage import download_blob, decrypt_blob
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

# Sync engine for Celery (Celery doesn't play well with asyncio)
SYNC_DB_URL = settings.DATABASE_URL
sync_engine = create_engine(SYNC_DB_URL)


def _update_job(session: Session, job_id: str, **kwargs):
    job = session.get(Job, job_id)
    if job:
        for k, v in kwargs.items():
            setattr(job, k, v)
        session.commit()


@celery_app.task(bind=True, name="app.tasks.proof_task.process_document")
def process_document(
    self,
    job_id: str,
    doc_id: str,
    s3_key: str,
    filename: str,
    encryption_key: str | None = None,
    encryption_iv: str | None = None,
):
    """Full pipeline: download -> OCR -> LLM -> ZK -> store result."""
    with Session(sync_engine) as session:
        try:
            _update_job(session, job_id, status=JobStatus.processing)

            # Step 1: Download encrypted blob
            logger.info(f"[{job_id}] Downloading blob {s3_key}")
            file_bytes = download_blob(s3_key)

            # Step 1b: Decrypt client-side AES-GCM payload before OCR
            file_bytes = decrypt_blob(file_bytes, encryption_key, encryption_iv)

            # Step 2: OCR / text extraction (in RAM only)
            logger.info(f"[{job_id}] Extracting text")
            document_text = extract_text_from_bytes(file_bytes, filename)
            del file_bytes  # free RAM immediately

            if not document_text.strip():
                raise ValueError("Could not extract any text from document")

            # Step 3: LLM claim extraction
            logger.info(f"[{job_id}] Extracting claims via LLM")
            raw_claims: ClaimSet = extract_claims(document_text)
            del document_text  # free RAM

            # Step 4: Validate and normalise
            claims = validate_and_normalise(raw_claims)

            # Step 5: ZK proof generation
            logger.info(f"[{job_id}] Generating ZK proof")
            proof, public_signals = generate_proof(claims)

            # Step 6: (Optional) on-chain submission — stubbed; 
            # real impl calls Web3/ethers to send tx
            # Unique mock tx hash per job to avoid repeated values in UI/demo mode.
            tx_hash = f"0x{uuid.uuid4().hex}{uuid.uuid4().hex}"[:66]
            bitmap = build_bitmap(claims)

            # Persist proof record
            proof_record = OnChainProof(
                id=str(uuid.uuid4()),
                user_address=session.get(Job, job_id).user_address,
                claim_bitmap=hex(bitmap),
                tx_hash=tx_hash,
            )
            session.add(proof_record)

            _update_job(
                session, job_id,
                status=JobStatus.done,
                claim_set=claims.model_dump(),
                proof_tx_hash=tx_hash,
            )
            logger.info(f"[{job_id}] Pipeline complete. tx={tx_hash}")

        except Exception as exc:
            logger.error(f"[{job_id}] Pipeline failed: {exc}", exc_info=True)
            _update_job(
                session, job_id,
                status=JobStatus.failed,
                error_message=str(exc),
            )
            raise exc
