import os
import json
import sys
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# --- ROBUST PATH FIX ---
# Get the absolute path of THIS script (scada_admin.py)
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level (to Keri-Anchor-Contract root) -> artifacts -> contracts -> ...
artifact_path = os.path.join(
    current_script_dir, 
    "..", 
    "artifacts", 
    "contracts", 
    "KERIAnchor.sol", 
    "KERIAnchor.json"
)

# CONFIG
RPC_URL = "http://127.0.0.1:8545"
ADMIN_PRIVATE_KEY = os.getenv("PRIVATE_KEY", "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

def revoke_gateway(target_aid):
    if not os.path.exists(artifact_path):
        print(f"❌ ERROR: Cannot find ABI file at:\n{artifact_path}")
        print("Did you run 'npx hardhat compile'?")
        return

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    with open(artifact_path, "r") as f:
        abi = json.load(f)["abi"]

    if not CONTRACT_ADDRESS:
        print("❌ ERROR: CONTRACT_ADDRESS not found in .env")
        return

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    account = w3.eth.account.from_key(ADMIN_PRIVATE_KEY)

    print(f"🚨 REVOKING IDENTITY: {target_aid}")
    
    try:
        tx = contract.functions.revokeDevice(target_aid).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 300000,
            'gasPrice': w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, ADMIN_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"⏳ Transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            print(f"✅ SUCCESS: {target_aid} is now REVOKED on Blockchain.")
        else:
            print("❌ FAILED: Transaction reverted.")
            
    except Exception as e:
        print(f"❌ Blockchain Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("Enter Gateway AID to Revoke: ")
    revoke_gateway(target)