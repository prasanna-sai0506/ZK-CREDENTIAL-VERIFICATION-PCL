#!/usr/bin/env python3
"""
CLI: Convert a ClaimSet JSON file to a Circom witness input JSON.

Usage:
    python claim_to_witness.py --claims '{"over_18":true,"nationality":"Indian"}' \
        --output witness_input.json
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.app.models.schemas import ClaimSet
from backend.app.services.zk_generator import claim_to_witness
from backend.app.services.claim_validator import validate_and_normalise


def main():
    parser = argparse.ArgumentParser(description="ClaimSet → Circom witness input")
    parser.add_argument("--claims", required=True, help="JSON string of ClaimSet")
    parser.add_argument("--output", default="witness_input.json", help="Output file path")
    args = parser.parse_args()

    raw = json.loads(args.claims)
    claim_set = ClaimSet(**raw)
    claim_set = validate_and_normalise(claim_set)
    witness = claim_to_witness(claim_set)

    with open(args.output, "w") as f:
        json.dump(witness, f, indent=2)

    print(f"✅  Witness written to {args.output}")
    print(json.dumps(witness, indent=2))


if __name__ == "__main__":
    main()
