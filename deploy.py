from web3 import Web3
from solcx import compile_standard, install_solc
import json
import os
from dotenv import load_dotenv

install_solc('v0.6.0')

load_dotenv()

with open("./contracts/Storage.sol", "r") as file:
  storage_contract = file.read()

compiled_storage_contract = compile_standard({
  "language": "Solidity",
  "sources": {"Storage.sol": {
      "content": storage_contract
    }
  },
  "settings": {
    "outputSelection": {
      "*": {
        "*": [
          "abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"
        ]
      }
    }
  }
}, solc_version="0.6.0")

with open("compiled_storage_contract.json", "w") as file:
  json.dump(compiled_storage_contract, file)

bytecode = compiled_storage_contract["contracts"][
  "Storage.sol"]["Storage"]["evm"]["bytecode"]["object"]

abi = compiled_storage_contract["contracts"]["Storage.sol"]["Storage"]["abi"]

# Connect to rinkeby
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

chain_id = int(os.getenv("CHAIN_ID"))
address = os.getenv("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
print("Deploying contract...")
Storage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(address)

txn = Storage.constructor().buildTransaction(
  {"chainId": chain_id, "from": address, "nonce": nonce, "gasPrice": w3.eth.gas_price})

signed_txn = w3.eth.account.sign_transaction(txn, private_key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Contract deployed!")

# Interact with the contract
# You always need the contract address and the abi
print("Updating the contract...")
storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

store_txn = storage.functions.set(99).buildTransaction(
  {"chainId": chain_id, "from": address, "nonce": nonce + 1, "gasPrice": w3.eth.gas_price})
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)
print("Contract updated!")
