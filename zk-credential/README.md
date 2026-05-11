# ZK Credential Verification

> **LLM-driven claim extraction as input to a ZK circuit, enabling document-agnostic on-chain identity.**

A user uploads any identity document (passport, degree, employment letter). An LLM extracts structured claims. These claims feed into a Circom Groth16 ZK circuit. The proof is posted on-chain. Third-party verifiers check the proof — **they never see the raw document**.

---

## Architecture

```
User Browser  →  FastAPI  →  Celery  →  LLM Parser  →  ZK Generator  →  EVM Contract
     ↑ AES-256-GCM encrypted upload                         ↑ Groth16 proof
     └─────────────────── JWT auth ──────────────────────────┘
```

**Stack:** React 18 + Vite · FastAPI · Celery + Redis · PostgreSQL · GPT-4o/LLaMA · Circom 2.1 · snarkjs · Solidity + Hardhat

---

## Quick Start

```bash
cp .env.example .env       # fill in API keys
docker-compose up -d       # starts all services
open http://localhost:5173
```

---

## Build Phases

### Phase 1 — Local Dev
```bash
docker-compose up -d
```

### Phase 2 — Compile ZK Circuit
```bash
npm install -g circom snarkjs
bash scripts/compile_circuit.sh
```

### Phase 3 — Deploy Contract
```bash
cd contracts && npm install
npx hardhat run scripts/deploy.js --network sepolia
echo 'VERIFIER_ADDRESS=0x...' >> ../.env
```

### Phase 4 — Environment Config
See `.env.example` for all required variables.

### Phase 5 — End-to-End Smoke Test
```bash
python scripts/e2e_smoke.py \
  --doc testdata/sample_passport.pdf \
  --expected-claims '{"over_18":true,"nationality":"Indian"}' \
  --api-url http://localhost:8000
```

---

## Repository Structure

```
zk-credential/
├── frontend/src/
│   ├── components/    # UploadZone, ProofCard, WalletButton
│   ├── hooks/         # useProofStatus
│   ├── store/         # Zustand: walletStore, jobStore
│   └── pages/         # Upload, Dashboard, Verify
├── backend/app/
│   ├── api/           # FastAPI routes + JWT auth
│   ├── services/      # llm_parser, claim_validator, ocr_service, zk_generator, storage
│   ├── tasks/         # Celery: process_document pipeline
│   └── models/        # SQLAlchemy ORM + Pydantic schemas
├── circuits/
│   └── credential.circom   # Groth16 ZK circuit (~1,200 R1CS constraints)
├── contracts/
│   ├── CredentialVerifier.sol
│   ├── scripts/deploy.js
│   └── test/CredentialVerifier.test.js
├── scripts/
│   ├── compile_circuit.sh
│   ├── claim_to_witness.py
│   └── e2e_smoke.py
└── docker-compose.yml
```

---

## API Endpoints

| Endpoint | Auth | Description |
|---|---|---|
| `POST /api/v1/documents/upload` | JWT | Upload doc → returns `doc_id + job_id` |
| `GET /api/v1/jobs/{job_id}/status` | JWT | Poll: `queued│processing│done│failed` |
| `GET /api/v1/proofs/{user_address}` | Public | List on-chain proofs for address |
| `POST /api/v1/verify` | Public | Pass address + bitmap → `true/false` |
| `DELETE /api/v1/documents/{doc_id}` | JWT | Right to erasure |
| `GET /api/v1/health` | None | Liveness check |

---

## Security Model

| Threat | Severity | Mitigation |
|---|---|---|
| LLM hallucinated claims | HIGH | Multi-model cross-check, Pydantic strict validation |
| Fake document upload | HIGH | External notarisation (out-of-scope for ZK layer) |
| Proving key compromise | MED | MPC trusted setup ceremony |
| Server-side plaintext leak | MED | Zero plaintext persistence; RAM only |
| Proof replay attack | LOW | Nullifier set in contract |

---

## Claim Bitmap

| Bit | Claim |
|---|---|
| 0 | `over_18` |
| 1 | `nationality` present |
| 2 | `has_degree` present |
| 3 | `employment_verified` |

---

## Patent Angle

LLM-driven claim extraction as input to a ZK circuit, enabling **document-agnostic on-chain identity**. The decoupling of *parsing* (LLM) from *proving* (ZK) is the novel technical contribution.
