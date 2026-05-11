from pydantic import BaseModel, Field
from typing import Optional, Any
import datetime

# ─── Claim Schema ───────────────────────────────────────────────────────────

class ClaimSet(BaseModel):
    model_config = {"strict": False}

    over_18: Optional[bool] = None
    nationality: Optional[str] = None        # 'Indian', 'American', ...
    has_degree: Optional[str] = None         # 'CS', 'Law', 'Medicine', ...
    degree_institution: Optional[str] = None
    employment_verified: Optional[bool] = None
    custom_claims: dict[str, Any] = Field(default_factory=dict)


# ─── API Schemas ─────────────────────────────────────────────────────────────

class UploadResponse(BaseModel):
    doc_id: str
    job_id: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    claim_set: Optional[dict] = None
    proof_tx_hash: Optional[str] = None
    error_message: Optional[str] = None

class ProofEntry(BaseModel):
    claim_bitmap: str
    tx_hash: str
    created_at: datetime.datetime

class VerifyRequest(BaseModel):
    user_address: str
    claim_bitmap: str  # hex string

class VerifyResponse(BaseModel):
    verified: bool

class DeleteResponse(BaseModel):
    deleted: bool

class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
