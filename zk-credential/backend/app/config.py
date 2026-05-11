from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://zkuser:zkpassword@localhost:5432/zkcredential"
    REDIS_URL: str = "redis://localhost:6379"
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    S3_BUCKET: str = "zk-cred-docs"
    ZK_CIRCUIT_PATH: str = "./circuits/build"
    VERIFIER_ADDRESS: str = "0x0000000000000000000000000000000000000000"
    ENCRYPTION_KEY: str = "0" * 64  # 32-byte hex
    JWT_SECRET: str = "supersecretjwtkey"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24h
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    HEURISTIC_FALLBACK_ENABLED: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
