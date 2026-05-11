"""
All FastAPI route handlers.
"""

import uuid
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.database import get_db, Document, Job, OnChainProof, JobStatus
from app.models.schemas import (
    UploadResponse, JobStatusResponse, ProofEntry,
    VerifyRequest, VerifyResponse, DeleteResponse, HealthResponse,
)
from app.services.storage import upload_encrypted_blob, delete_blob
from app.tasks.proof_task import process_document
from app.api.auth import get_current_user, create_access_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1")

MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 MB


# ─── Auth ────────────────────────────────────────────────────────────────────

@router.post("/auth/token")
async def get_token(user_address: str):
    """Issue a JWT for a wallet address (simplified — real app uses wallet signature)."""
    return {"access_token": create_access_token(user_address), "token_type": "bearer"}


# ─── Documents ───────────────────────────────────────────────────────────────

@router.post("/documents/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    encryption_key: str | None = Form(default=None),
    encryption_iv: str | None = Form(default=None),
    db: AsyncSession = Depends(get_db),
    user_address: str = Depends(get_current_user),
):
    """
    Accept AES-256-GCM encrypted document from client.
    Store to S3. Enqueue Celery proving job.
    """
    file_bytes = await file.read()
    if len(file_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 20 MB)")

    doc_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())

    # Store encrypted blob
    s3_key = upload_encrypted_blob(file_bytes, doc_id, file.filename or "document")

    # Persist document record
    doc = Document(doc_id=doc_id, user_address=user_address, s3_key=s3_key)
    db.add(doc)

    # Persist job record
    job = Job(job_id=job_id, doc_id=doc_id, user_address=user_address)
    db.add(job)
    await db.commit()

    # Enqueue async task
    process_document.delay(
        job_id,
        doc_id,
        s3_key,
        file.filename or "document",
        encryption_key,
        encryption_iv,
    )
    logger.info(f"Enqueued job {job_id} for doc {doc_id}")

    return UploadResponse(doc_id=doc_id, job_id=job_id)


@router.delete("/documents/{doc_id}", response_model=DeleteResponse)
async def delete_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
    user_address: str = Depends(get_current_user),
):
    """Right to erasure — deletes encrypted blob from S3."""
    result = await db.execute(select(Document).where(Document.doc_id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.user_address != user_address:
        raise HTTPException(status_code=403, detail="Not your document")

    delete_blob(doc.s3_key)
    await db.delete(doc)
    await db.commit()
    return DeleteResponse(deleted=True)


# ─── Jobs ────────────────────────────────────────────────────────────────────

@router.get("/jobs/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user_address: str = Depends(get_current_user),
):
    result = await db.execute(select(Job).where(Job.job_id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.user_address != user_address:
        raise HTTPException(status_code=403, detail="Not your job")

    return JobStatusResponse(
        job_id=job_id,
        status=job.status,
        claim_set=job.claim_set,
        proof_tx_hash=job.proof_tx_hash,
        error_message=job.error_message,
    )


# ─── Proofs ──────────────────────────────────────────────────────────────────

@router.get("/proofs/{user_address}", response_model=List[ProofEntry])
async def get_proofs(user_address: str, db: AsyncSession = Depends(get_db)):
    """Public: list on-chain proofs for a wallet address."""
    result = await db.execute(
        select(OnChainProof).where(OnChainProof.user_address == user_address)
    )
    proofs = result.scalars().all()
    return [
        ProofEntry(claim_bitmap=p.claim_bitmap, tx_hash=p.tx_hash, created_at=p.created_at)
        for p in proofs
    ]


@router.post("/verify", response_model=VerifyResponse)
async def verify_claims(body: VerifyRequest, db: AsyncSession = Depends(get_db)):
    """Check if address has a proof matching the requested claim bitmap."""
    result = await db.execute(
        select(OnChainProof).where(
            OnChainProof.user_address == body.user_address,
            OnChainProof.claim_bitmap == body.claim_bitmap,
        )
    )
    proof = result.scalar_one_or_none()
    return VerifyResponse(verified=proof is not None)


# ─── Health ──────────────────────────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse)
async def health(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    try:
        await db.execute(select(1))
    except Exception:
        db_status = "error"

    return HealthResponse(status="ok", database=db_status, redis="ok")
