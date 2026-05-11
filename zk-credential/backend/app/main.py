from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.models.database import init_db
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="ZK Credential Verification API",
    description="LLM-powered claim extraction + Groth16 ZK proofs",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
async def startup():
    await init_db()
