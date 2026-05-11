#!/usr/bin/env bash
# Compile Circom circuit and run trusted setup for Groth16
set -euo pipefail

CIRCUIT_DIR="$(cd "$(dirname "$0")/../circuits" && pwd)"
BUILD_DIR="$CIRCUIT_DIR/build"
CONTRACTS_DIR="$(cd "$(dirname "$0")/../contracts" && pwd)"

mkdir -p "$BUILD_DIR"
cd "$CIRCUIT_DIR"

echo "=== [1/6] Compiling circuit ==="
circom credential.circom --r1cs --wasm --sym -o "$BUILD_DIR/"

echo "=== [2/6] Powers of Tau (phase 1) ==="
snarkjs powersoftau new bn128 12 "$BUILD_DIR/pot12_0000.ptau" -v
snarkjs powersoftau contribute "$BUILD_DIR/pot12_0000.ptau" "$BUILD_DIR/pot12_0001.ptau" \
    --name="First contribution" -v -e="$(head -c 64 /dev/urandom | xxd -p)"

echo "=== [3/6] Prepare phase 2 ==="
snarkjs powersoftau prepare phase2 "$BUILD_DIR/pot12_0001.ptau" "$BUILD_DIR/pot12_final.ptau" -v

echo "=== [4/6] Circuit-specific setup (Groth16) ==="
snarkjs groth16 setup "$BUILD_DIR/credential.r1cs" "$BUILD_DIR/pot12_final.ptau" "$BUILD_DIR/cred_0000.zkey"
snarkjs zkey contribute "$BUILD_DIR/cred_0000.zkey" "$BUILD_DIR/cred_final.zkey" \
    --name="Second contribution" -v -e="$(head -c 64 /dev/urandom | xxd -p)"

echo "=== [5/6] Export verification key ==="
snarkjs zkey export verificationkey "$BUILD_DIR/cred_final.zkey" "$BUILD_DIR/verification_key.json"

echo "=== [6/6] Export Solidity verifier ==="
snarkjs zkey export solidityverifier "$BUILD_DIR/cred_final.zkey" \
    "$CONTRACTS_DIR/CredentialVerifierBase.sol"

echo ""
echo "✅  Circuit compiled. Artifacts in $BUILD_DIR"
echo "    verification_key.json → share this with verifiers"
echo "    cred_final.zkey       → keep secret on proving server"
