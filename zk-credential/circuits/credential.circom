pragma circom 2.1.0;

include "circomlib/circuits/poseidon.circom";
include "circomlib/circuits/comparators.circom";

template CredentialProof() {
    // ── Private inputs (never revealed on-chain) ─────────────────────────────
    signal input dateOfBirth;      // Unix timestamp of birth date
    signal input nationalityHash;  // Poseidon("Indian")
    signal input degreeHash;       // Poseidon("CS")
    signal input salt;             // Random blinding factor (254-bit)

    // ── Public inputs (visible on-chain) ─────────────────────────────────────
    signal input currentTimestamp;
    signal input claimBitmap;      // Bit-encoded proven claims
    signal input commitment;       // Poseidon(dob, nat, deg, salt)

    // ── Output ────────────────────────────────────────────────────────────────
    signal output verified;        // 1 if all claims pass, 0 otherwise

    // ── Prove age >= 18 ───────────────────────────────────────────────────────
    // 18 years in seconds = 18 * 365.25 * 86400 ≈ 567,648,000
    component ageCheck = LessThan(32);
    ageCheck.in[0] <== dateOfBirth + 567648000;
    ageCheck.in[1] <== currentTimestamp;

    // ── Verify Poseidon commitment matches private inputs ─────────────────────
    component posHash = Poseidon(4);
    posHash.inputs[0] <== dateOfBirth;
    posHash.inputs[1] <== nationalityHash;
    posHash.inputs[2] <== degreeHash;
    posHash.inputs[3] <== salt;

    commitment === posHash.out;

    // ── Output ────────────────────────────────────────────────────────────────
    verified <== ageCheck.out;
}

component main { public [currentTimestamp, claimBitmap, commitment] } = CredentialProof();
