# -*- coding: utf-8 -*-
import json
from sqlite3 import Timestamp
import sys
from web3 import Web3
import numpy as np
from brownie.convert import to_uint

# ropsten
my_contract_addr = "****"
attack_contract = ""
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/***"))


chain_id = 3
my_address = "***"
private_key = "****"
nonce = w3.eth.getTransactionCount(my_address)
abi_str = """[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"name": "callFuct",
		"outputs": [],
		"stateMutability": "payable",
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
		"inputs": [],
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
		"name": "answer",
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
		"name": "check",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "get_guess",
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
contract = w3.eth.contract(address=my_contract_addr, abi=abi)
print(contract)
print(f"get all functions: {contract.all_functions()}")
curr_balance = w3.eth.get_balance(my_contract_addr)
print(f"get contract balance: {curr_balance}")


print("will call functions callFuct and send 1 eth..")

contract_transaction = contract.functions.callFuct(attack_contract).buildTransaction(
    {
        "chainId": chain_id,
        # "gasPrice": w3.eth.gas_price * 5,
        "value": Web3.toWei(1, "ether"),
        "from": my_address,
        "nonce": nonce,
        "maxFeePerGas": 2000000000,
        "maxPriorityFeePerGas": 1000000000,
    }
)

signed_contract_txn = w3.eth.account.sign_transaction(
    contract_transaction, private_key=private_key
)
tx_contract_hash = w3.eth.send_raw_transaction(signed_contract_txn.rawTransaction)
print(f"calling  func...: {tx_contract_hash.hex()}")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_contract_hash)

curr_balance = w3.eth.get_balance(contract_addr)
print(f"get contract balance: {curr_balance}")
