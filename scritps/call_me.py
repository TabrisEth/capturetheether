import json
from web3 import Web3

contract_addr = ""
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/***"))
chain_id = 3
my_address = "***"
private_key = "***"
nonce = w3.eth.getTransactionCount(my_address)
abi_str = """
[{"constant":false,"inputs":[],"name":"callme","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"isComplete","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]
"""

abi = json.loads(abi_str)
# Working with deployed Contracts
contract = w3.eth.contract(address=contract_addr, abi=abi)
print(contract)
print(f"get all functions: {contract.all_functions()}")
print(f"get isComplete default value: {contract.functions.isComplete().call()}")
print("will call functions call_me..")

contract_transaction = contract.functions.callme().buildTransaction(
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
print("calling call me func...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_contract_hash)

print(f"get isComplete  value: {contract.functions.isComplete().call()}")
