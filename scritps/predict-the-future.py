# -*- coding: utf-8 -*-
import json
from sqlite3 import Timestamp
import sys
import time
from web3 import Web3
import numpy as np
from brownie.convert import to_uint

# ropsten
contract_addr = "***"
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/***"))

chain_id = 3
my_address = "***"
private_key = "***"
nonce = w3.eth.getTransactionCount(my_address)
abi_str = """[
	{
		"inputs": [],
		"name": "callLockInGuess",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "callsettle",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "deposit",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "_to",
				"type": "address"
			}
		],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "_interface",
		"outputs": [
			{
				"internalType": "contract PredictTheFutureChallenge",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "lucknumber",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""
abi = json.loads(abi_str)
# Working with deployed Contracts
contract = w3.eth.contract(address=contract_addr, abi=abi)
print(contract)
print(f"get all functions: {contract.all_functions()}")


print("will call functions callsettle..")
while True:
    try:
        print("will reconnect contract...")
        contract = w3.eth.contract(address=contract_addr, abi=abi)
        # print(contract)
        # print(f"get all functions: {contract.all_functions()}")
        nonce = nonce + 1
        contract_transaction = contract.functions.callsettle().buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price * 5,
                "from": my_address,
                "nonce": nonce,
            }
        )
        break
    except:
        print(f"will sleep 10 sec..{nonce}")
        time.sleep(10)

signed_contract_txn = w3.eth.account.sign_transaction(
    contract_transaction, private_key=private_key
)
tx_contract_hash = w3.eth.send_raw_transaction(signed_contract_txn.rawTransaction)
print(f"calling callsettle func...: {tx_contract_hash.hex()}")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_contract_hash)
