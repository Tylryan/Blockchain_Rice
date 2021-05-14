#!/usr/bin/python3

# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os
# Import constants.py and necessary functions from bit and web3
from constants import *
from web3 import Web3
from eth_account import Account
import bit
from time import sleep
from rich.traceback import install
from pprint import pprint
os.chdir('./hd-wallet-derive')
install()
# Load and set environment variables
load_dotenv()
# Getting the mnemonic from .env works
mnemonic = os.getenv("MNEMONIC")

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
# Create a function called `derive_wallets`

# Works


def derive_wallets(mnemonic, coin_type):
    # Command Works
    command = f'./derive -g --coin={coin_type} --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --numderive=3 --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a DICTIONARY object called coins to store the output from `derive_wallets`.
# coin_types = [BTC, ETH, BTCTEST]
# all_coin_data = {}
# for i in coin_types:
#     if i == 'btc':
#         pass
#     else:
#         all_coin_data[i] = derive_wallets(mnemonic, i)


# def to_account(coin, private_key):
#     switch = {
#         "eth": Account.from_key(private_key).address,
#         "btc-test": bit.PrivateKeyTestnet(private_key)
#     }

#     return switch[coin]

# Since we are only using two coins, this is an easy way to determine which one to return.

# def private_key_to_account(coin_data):
#     addresses = {}
#     for coin, data in all_coin_data.items():
#         # Find private key
#         if coin == 'btc-test':
#             # Find the private key
#             private_key = data[0]['privkey']
#             # Return an account associated with that private key
#             account = bit.PrivateKeyTestnet(private_key)
#             # Add that account to the dictionary associated with that coin
#             addresses[coin] = private_key
#         elif coin == 'eth':
#             private_key = data[0]['privkey']
#             account = Account.privateKeyToAccount(private_key)
#             addresses[coin] = private_key
#     return addresses

# # Put private key and coin type into to_account function
# addresses[coin] = to_account(coin, private_key)


def create_tx(coin, account, recipient, amount):
    if coin == 'eth':
        gasEstimate = w3.eth.estimateGas(
            {
                "coin": coin,
                "from": account.address,
                "to": recipient,
                "value": amount
            }
        )
        return {
            # Ganache
            'chainId': 5777,
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    elif coin == 'btc-test':
        bit.PrivateKeyTestnet.prepare_transaction(
            account.address,
            [(recipient, amount, coin)]
        )


def send_tx(coin, account, amount, recipient):
    # Create the transaction
    transaction = create_tx(
        coin,
        account,
        recipient,
        amount
    )

    # Sign the transaction
    sign_tx = account.sign_transaction(transaction)
    # The transaction's hash
    if coin == 'eth':
        result = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
    elif coin == 'btc-test':
        result = bit.NetworkAPI.broadcast_tx_testnet(sign_tx)
    print(f"This is your hash number: {result.hex()}")
    return result.hex()


coin_type = input('Enter "ETH" or don\'t bother :) ----> ').lower()
mnemonic = input('Please enter your mnemonic:\n ----> ')
amount = int(input('How much Ether Would you like to send?: '))
recipient = input(f'Which account would you like to send {amount} ETH to? ')
private_key = derive_wallets(mnemonic, coin_type)[0]['privkey']

account_key = Account.from_key(
    private_key) or bit.PrivateKeyTestnet(private_key)

send_tx(
    coin_type,
    account_key,
    amount,
    recipient
)

print('Sending the transaction over....')
print('Check your Ganache account for the receipt')
sleep(30)
# account_addresses = private_key_to_account(all_coin_data)
# print(account_addresses)

# transaction = create_tx(account_address)
