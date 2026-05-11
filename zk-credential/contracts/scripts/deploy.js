const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);
  const Factory = await hre.ethers.getContractFactory("CredentialVerifier");
  const verifier = await Factory.deploy();
  await verifier.waitForDeployment();
  const address = await verifier.getAddress();
  console.log("CredentialVerifier deployed to:", address);
  fs.writeFileSync(
    path.join(__dirname, "../deployment.json"),
    JSON.stringify({ network: hre.network.name, address, deployer: deployer.address, timestamp: new Date().toISOString() }, null, 2)
  );
}
main().catch(e => { console.error(e); process.exit(1); });
