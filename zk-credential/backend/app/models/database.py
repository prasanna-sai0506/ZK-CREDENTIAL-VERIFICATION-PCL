from sqlalchemy import Column, String, DateTime, JSON, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import enum
import datetime
from app.config import settings

Base = declarative_base()

# Convert sync URL to async
DB_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DB_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class JobStatus(str, enum.Enum):
    queued = "queued"
    processing = "processing"
    done = "done"
    failed = "failed"

class Document(Base):
    __tablename__ = "documents"
    doc_id = Column(String, primary_key=True)
    user_address = Column(String, nullable=False, index=True)
    s3_key = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(String, primary_key=True)
    doc_id = Column(String, nullable=False, index=True)
    user_address = Column(String, nullable=False, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.queued)
    claim_set = Column(JSON, nullable=True)
    proof_tx_hash = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class OnChainProof(Base):
    __tablename__ = "onchain_proofs"
    id = Column(String, primary_key=True)
    user_address = Column(String, nullable=False, index=True)
    claim_bitmap = Column(String, nullable=False)
    tx_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
