"""
Storage Service — S3 for encrypted blobs.
Falls back to local /tmp storage if AWS not configured (dev mode).
"""

import io
import logging
import os
import uuid
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.config import settings

logger = logging.getLogger(__name__)

LOCAL_FALLBACK_DIR = Path("/tmp/zk-cred-blobs")


def upload_encrypted_blob(file_bytes: bytes, doc_id: str, filename: str) -> str:
    """Upload encrypted blob. Returns S3 key (or local path)."""
    key = f"docs/{doc_id}/{filename}"

    if settings.AWS_ACCESS_KEY_ID:
        import boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        s3.upload_fileobj(io.BytesIO(file_bytes), settings.S3_BUCKET, key)
        logger.info(f"Uploaded to S3: s3://{settings.S3_BUCKET}/{key}")
    else:
        # Local fallback
        local_path = LOCAL_FALLBACK_DIR / doc_id
        local_path.mkdir(parents=True, exist_ok=True)
        (local_path / filename).write_bytes(file_bytes)
        logger.info(f"Stored locally (no S3 configured): {local_path / filename}")

    return key


def download_blob(s3_key: str) -> bytes:
    """Download encrypted blob from S3 (or local fallback)."""
    if settings.AWS_ACCESS_KEY_ID:
        import boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        buf = io.BytesIO()
        s3.download_fileobj(settings.S3_BUCKET, s3_key, buf)
        return buf.getvalue()
    else:
        # Local fallback: key = "docs/{doc_id}/{filename}"
        parts = s3_key.split("/")
        local_path = LOCAL_FALLBACK_DIR / parts[1] / parts[2]
        return local_path.read_bytes()


def delete_blob(s3_key: str) -> None:
    """Delete blob (right to erasure)."""
    if settings.AWS_ACCESS_KEY_ID:
        import boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        s3.delete_object(Bucket=settings.S3_BUCKET, Key=s3_key)
    else:
        parts = s3_key.split("/")
        local_path = LOCAL_FALLBACK_DIR / parts[1] / parts[2]
        if local_path.exists():
            local_path.unlink()


def decrypt_blob(file_bytes: bytes, encryption_key: str | None, encryption_iv: str | None) -> bytes:
    """Decrypt client-side AES-GCM ciphertext when key material is provided."""
    if not encryption_key or not encryption_iv:
        return file_bytes

    key_bytes = bytes.fromhex(encryption_key)
    iv_bytes = bytes.fromhex(encryption_iv)
    aesgcm = AESGCM(key_bytes)
    return aesgcm.decrypt(iv_bytes, file_bytes, None)
