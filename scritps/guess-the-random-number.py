# -*- coding: utf-8 -*-
import json
from sqlite3 import Timestamp
import sys
from web3 import Web3
import numpy as np
from brownie.convert import to_uint

# ropsten
contract_addr = "***"
block_id = ***
w3 = Web3(
    Web3.HTTPProvider("https://ropsten.infura.io/v3/***")
)

# Looking up transactions
# tx = "0x852ed57dff8bf6db6f6764a9fdf6aa5e6cf09a944d5ab6847ce0de913dfd6fe0"
# w3.eth.get_transaction(tx)
number = w3.eth.get_storage_at(
    contract_addr,
    0,
).hex()
answerNum = int(number, 16)


chain_id = 3
my_address = "**"
private_key = "***"
nonce = w3.eth.getTransactionCount(my_address)
abi_str = """[{"constant":false,"inputs":[{"name":"n","type":"uint8"}],"name":"guess","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"isComplete","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":true,"stateMutability":"payable","type":"constructor"}]"""

abi = json.loads(abi_str)
# Working with deployed Contracts
contract = w3.eth.contract(address=contract_addr, abi=abi)
print(contract)
print(f"get all functions: {contract.all_functions()}")
curr_balance = w3.eth.get_balance(contract_addr)
print(f"get contract balance: {curr_balance}")


print("will call functions guess and send 1 eth..")

contract_transaction = contract.functions.guess(answerNum).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price * 5,
        "value": Web3.toWei(1, "ether"),
        "from": my_address,
        "nonce": nonce,
    }
)

signed_contract_txn = w3.eth.account.sign_transaction(
    contract_transaction, private_key=private_key
)
tx_contract_hash = w3.eth.send_raw_transaction(signed_contract_txn.rawTransaction)
print(f"calling guess func...: {tx_contract_hash.hex()}")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_contract_hash)

curr_balance = w3.eth.get_balance(contract_addr)
print(f"get contract balance: {curr_balance}")
