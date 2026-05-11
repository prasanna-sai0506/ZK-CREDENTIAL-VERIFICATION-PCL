"""
ZK Proof Generator
- Converts ClaimSet -> witness.json
- Runs snarkjs groth16.prove via subprocess
- Returns proof.json + public.json as dicts
"""

import json
import logging
import secrets
import subprocess
import tempfile
import time
from pathlib import Path

from app.config import settings
from app.models.schemas import ClaimSet
from app.services.claim_validator import build_bitmap

logger = logging.getLogger(__name__)


def _poseidon_hash_py(value: int | bytes) -> int:
    """
    Lightweight Poseidon hash stub for witness generation.
    In production use circomlibjs or poseidon-hash library.
    """
    try:
        # Try real poseidon_hash library
        from poseidon import poseidon
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big") % (2**254)
        return poseidon([value])
    except ImportError:
        # Deterministic fallback using Python hash (NOT cryptographically secure)
        # Replace with real Poseidon in production
        if isinstance(value, bytes):
            value = int.from_bytes(value, "big") % (2**254)
        import hashlib
        h = hashlib.sha256(str(value).encode()).digest()
        return int.from_bytes(h, "big") % (2**254 - 1)


def claim_to_witness(claim_set: ClaimSet) -> dict:
    """Convert a validated ClaimSet into a Circom witness dict."""
    salt = secrets.randbits(254)

    # Date of birth: if not present use 0 (claim not proven)
    dob = 0  # Placeholder; real implementation reads from document metadata

    nat_bytes = (claim_set.nationality or "").encode("utf-8")
    nat_hash = _poseidon_hash_py(nat_bytes) if nat_bytes else 0

    deg_bytes = (claim_set.has_degree or "").encode("utf-8")
    deg_hash = _poseidon_hash_py(deg_bytes) if deg_bytes else 0

    current_ts = int(time.time())
    bitmap = build_bitmap(claim_set)

    # Commitment = Poseidon(dob, nat, deg, salt)
    # Simplified: hash pairwise
    commitment = _poseidon_hash_py(dob ^ nat_hash ^ deg_hash ^ salt)

    return {
        "dateOfBirth": str(dob),
        "nationalityHash": str(nat_hash),
        "degreeHash": str(deg_hash),
        "salt": str(salt),
        "currentTimestamp": str(current_ts),
        "claimBitmap": str(bitmap),
        "commitment": str(commitment),
    }


def generate_proof(claim_set: ClaimSet) -> tuple[dict, dict]:
    """
    Generate a Groth16 ZK proof.
    Returns (proof_dict, public_signals_dict).
    
    Requires:
      - snarkjs installed (npm install -g snarkjs)
      - circuits/build/credential_js/credential.wasm
      - circuits/build/cred_final.zkey
    """
    circuit_path = Path(settings.ZK_CIRCUIT_PATH)
    wasm_path = circuit_path / "credential_js" / "credential.wasm"
    zkey_path = circuit_path / "cred_final.zkey"

    if not wasm_path.exists() or not zkey_path.exists():
        logger.warning(
            "Circuit files not found at %s. Returning mock proof for development.",
            circuit_path,
        )
        return _mock_proof(claim_set)

    witness = claim_to_witness(claim_set)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        witness_file = tmp / "witness.json"
        witness_input_file = tmp / "input.json"
        proof_file = tmp / "proof.json"
        public_file = tmp / "public.json"

        witness_input_file.write_text(json.dumps(witness))

        # Generate witness
        subprocess.run(
            [
                "node",
                str(wasm_path.parent / "generate_witness.js"),
                str(wasm_path),
                str(witness_input_file),
                str(witness_file),
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )

        # Generate proof
        subprocess.run(
            [
                "snarkjs",
                "groth16",
                "prove",
                str(zkey_path),
                str(witness_file),
                str(proof_file),
                str(public_file),
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )

        proof = json.loads(proof_file.read_text())
        public = json.loads(public_file.read_text())

    logger.info("ZK proof generated successfully")
    return proof, public


def _mock_proof(claim_set: ClaimSet) -> tuple[dict, dict]:
    """Mock proof for development/testing when circuit files not compiled yet."""
    bitmap = build_bitmap(claim_set)
    witness = claim_to_witness(claim_set)
    mock_proof = {
        "pi_a": ["0x1234", "0x5678", "0x1"],
        "pi_b": [["0xabcd", "0xef01"], ["0x2345", "0x6789"], ["0x1", "0x0"]],
        "pi_c": ["0x9abc", "0xdef0", "0x1"],
        "protocol": "groth16",
        "curve": "bn128",
    }
    mock_public = [
        witness["currentTimestamp"],
        witness["claimBitmap"],
        witness["commitment"],
    ]
    return mock_proof, mock_public
