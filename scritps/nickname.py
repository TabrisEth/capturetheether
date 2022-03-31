import json
import sys
from web3 import Web3
from solcx import compile_standard, install_solc

new_nickname = "Tabris.eth"
with open("../contracts/NickName.sol", "r") as file:
    nickname_file = file.read()

# print("Installing...")
# install_solc("0.4.21")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"NickName.sol": {"content": nickname_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.4.21",
)

with open("nickname_compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get abi
abi = json.loads(
    compiled_sol["contracts"]["NickName.sol"]["CaptureTheEther"]["metadata"]
)["output"]["abi"]


contract_addr = "***"
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/***"))
chain_id = 3
my_address = "**"
private_key = "****"
nonce = w3.eth.getTransactionCount(my_address)

# Working with deployed Contracts
contract = w3.eth.contract(address=contract_addr, abi=abi)
print(contract)
print(f"get all functions: {contract.all_functions()}")
nickname = contract.functions.nicknameOf(my_address).call()
print(f"get curr myaddress nickname: {nickname.decode('UTF-8')}")

print(f"will call functions setNickname to: {new_nickname}")

contract_transaction = contract.functions.setNickname(
    str.encode(new_nickname)
).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_contract_txn = w3.eth.account.sign_transaction(
    contract_transaction, private_key=private_key
)
tx_contract_hash = w3.eth.send_raw_transaction(signed_contract_txn.rawTransaction)
print("calling setNickname func...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_contract_hash)
nickname = contract.functions.nicknameOf(my_address).call()
print(f"get new myaddress nickname: {nickname.decode('UTF-8')}")
