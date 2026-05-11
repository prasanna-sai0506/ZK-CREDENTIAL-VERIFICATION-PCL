#!/usr/bin/env python3
"""
End-to-end smoke test.

Usage:
    python e2e_smoke.py \
        --doc testdata/sample_passport.pdf \
        --expected-claims '{"over_18":true,"nationality":"Indian"}' \
        --api-url http://localhost:8000 \
        --user-address 0xTestAddress
"""

import argparse
import json
import sys
import time
import httpx

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", required=True)
    parser.add_argument("--expected-claims", required=True)
    parser.add_argument("--api-url", default="http://localhost:8000")
    parser.add_argument("--user-address", default="0xSmokeTestAddress")
    args = parser.parse_args()

    expected = json.loads(args.expected_claims)
    base = args.api_url

    print("=== ZK Credential E2E Smoke Test ===\n")

    # 1. Get token
    print(f"[1] Getting JWT for {args.user_address}")
    r = httpx.post(f"{base}/api/v1/auth/token", params={"user_address": args.user_address})
    r.raise_for_status()
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("    ✅ Token obtained\n")

    # 2. Upload document
    print(f"[2] Uploading document: {args.doc}")
    with open(args.doc, "rb") as f:
        r = httpx.post(f"{base}/api/v1/documents/upload",
                       files={"file": (args.doc, f, "application/octet-stream")},
                       headers=headers, timeout=30)
    r.raise_for_status()
    upload = r.json()
    job_id = upload["job_id"]
    doc_id = upload["doc_id"]
    print(f"    ✅ doc_id={doc_id}  job_id={job_id}\n")

    # 3. Poll for job completion
    print(f"[3] Polling job {job_id}...")
    for attempt in range(60):
        r = httpx.get(f"{base}/api/v1/jobs/{job_id}/status", headers=headers)
        r.raise_for_status()
        status_data = r.json()
        status = status_data["status"]
        print(f"    attempt {attempt+1}: {status}")
        if status == "done":
            break
        if status == "failed":
            print(f"    ❌ Job failed: {status_data.get('error_message')}")
            sys.exit(1)
        time.sleep(3)
    else:
        print("    ❌ Timed out waiting for proof")
        sys.exit(1)

    # 4. Validate claims
    print("\n[4] Validating extracted claims")
    claim_set = status_data.get("claim_set", {})
    for key, expected_val in expected.items():
        actual = claim_set.get(key)
        ok = "✅" if actual == expected_val else "❌"
        print(f"    {ok}  {key}: expected={expected_val}  actual={actual}")

    print(f"\n[5] Proof tx hash: {status_data.get('proof_tx_hash')}")
    print("\n=== Smoke test complete ===")

if __name__ == "__main__":
    main()
