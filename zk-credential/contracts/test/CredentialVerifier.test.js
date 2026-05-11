const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CredentialVerifier", function () {
  let verifier, user;
  beforeEach(async () => {
    [, user] = await ethers.getSigners();
    verifier = await (await ethers.getContractFactory("CredentialVerifier")).deploy();
  });

  it("deploys", async () => {
    expect(await verifier.getAddress()).to.match(/^0x[0-9a-fA-F]{40}$/);
  });

  it("verifies proof and stores bitmap", async () => {
    const proof = { pi_a: [1n, 2n], pi_b: [[3n, 4n],[5n, 6n]], pi_c: [7n, 8n] };
    const ts = BigInt(Math.floor(Date.now() / 1000) - 30);
    await verifier.connect(user).verifyAndStore(proof, [ts, 3n, 12345n]);
    expect(await verifier.getClaimBitmap(user.address)).to.equal(3n);
    expect(await verifier.checkClaims(user.address, 1n)).to.be.true;
    expect(await verifier.checkClaims(user.address, 4n)).to.be.false;
  });

  it("rejects replay", async () => {
    const proof = { pi_a: [1n, 2n], pi_b: [[3n, 4n],[5n, 6n]], pi_c: [7n, 8n] };
    const ts = BigInt(Math.floor(Date.now() / 1000) - 10);
    await verifier.connect(user).verifyAndStore(proof, [ts, 1n, 999n]);
    await expect(verifier.connect(user).verifyAndStore(proof, [ts, 1n, 999n])).to.be.revertedWith("Proof already used");
  });

  it("rejects stale timestamp", async () => {
    const proof = { pi_a: [1n, 2n], pi_b: [[3n, 4n],[5n, 6n]], pi_c: [7n, 8n] };
    const stale = BigInt(Math.floor(Date.now() / 1000) - 7200);
    await expect(verifier.connect(user).verifyAndStore(proof, [stale, 1n, 11111n])).to.be.revertedWith("Stale timestamp");
  });
});
