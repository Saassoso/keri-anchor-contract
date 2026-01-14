# KERI Blockchain Anchor Smart Contract ⛓️

![Solidity](https://img.shields.io/badge/Solidity-0.8.20-black)
![Hardhat](https://img.shields.io/badge/Framework-Hardhat-yellow)

This is the **Blockchain Layer** of the system. It deploys the `KERIAnchor` smart contract, which acts as an immutable registry for KERI event hashes.

##  Smart Contract: `KERIAnchor.sol`

The contract provides a simple, secure storage for:
* **AID (Identity):** The ID of the drone.
* **Sequence Number:** The ordered number of the event.
* **SAID (Digest):** The cryptographic hash of the event data.

It uses `Ownable` to ensure only the authorized Bridge can write data, while anyone can verify it.

##  Setup & Deployment

##  System Installation (Required)

This project is part of a 2-repository system. To make them work together, please follow this exact folder structure:

1. **Create a Main System Folder**
   ```bash
   mkdir KERI-IT-OT-System
   cd KERI-IT-OT-System

```

2. **Clone Both Repositories Here**
```bash
git clone [https://github.com/Saassoso/keri-gateway-it-ot.git](https://github.com/Saassoso/keri-gateway-it-ot.git) gateway
git clone [https://github.com/Saassoso/keri-anchor-contract.git](https://github.com/Saassoso/keri-anchor-contract) contract

```


3. **Create Shared Environment**
* **Virtual Env:** Create `keri-env` in this main folder.
* **Config:** Create a `.env` file in this main folder.



**Final Structure:**

```text
KERI-IT-OT-System/         <-- YOU ARE HERE
├── .env                   <-- Shared Keys
├── keri-env/              <-- Shared Python Environment
├── contract/              <-- The Blockchain Repo
└── gateway/               <-- This Python Repo

```

### 1. Install Dependencies
```bash
npm install
npm install @openzeppelin/contracts

```

### 2. Start Local Blockchain

This spins up a local Ethereum network (Hardhat Node). **Keep this terminal open.**

```bash
npx hardhat node

```

### 3. Deploy the Contract

Open a **new terminal** and run the deployment script.

```bash
npx hardhat run scripts/deploy_keri.js --network localhost

```

### 4. Get the Address

After deployment, you will see output like:

> `KERIAnchor deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3`

Copy this address and paste it into the `CONTRACT_ADDRESS` field in your Python Gateway `.env` file.

---

## 🛠️ Commands

| Command | Description |
| --- | --- |
| `npx hardhat node` | Starts the local blockchain. |
| `npx hardhat compile` | Compiles the Solidity contracts. |
| `npx hardhat test` | Runs automated tests (if any). |
| `npx hardhat run scripts/deploy_keri.js` | Deploys the contract. |


