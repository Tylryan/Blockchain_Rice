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


# # Create a dictionary object called coins to store the output from `derive_wallets`.
coin_types = [BTC, ETH, BTCTEST]
coins = {}
for i in coin_types:
    coins[i] = derive_wallets(mnemonic, i)

# # # Create a function called `priv_key_to_account` that converts privkey strings to account objects.


# # Works
def whichAccount(coin, private_key):
    switch = {
        "btc": bit.PrivateKeyTestnet(private_key),
        'btc-test': bit.PrivateKeyTestnet(private_key),
        "eth": Account.privateKeyToAccount(private_key)
    }
    return coin, switch[coin]


privateKeys = []
# For key value in coins
for x, y in coins.items():
    # From index 0-3
    for i in range(3):
        private_keys = y[i]['privkey']
        privateKeys.append((x, private_keys))
accounts = []
for coin, private_key in privateKeys:
    coin = coin.strip()
    private_key = str(private_key).strip()
    try:
        coin, accounts = whichAccount(coin, private_key)
        print(coin, accounts)
        accounts.append((coin, accounts))
    except Exception as e:
        continue
print(accounts)

# coins_private_key = {}
# for i in coin_types:
#     for x in range(3):
#         private_key = coins[i][int(x)]['privkey']
#         coins_private_key[i] = whichAccount(i)

# print(coins_private_key)

# ETH_account = priv_key_to_account(private_key)


# # # Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.


# def create_tx(account, recipient, amount):
#     gasEstimate = w3.eth.estimateGas(
#         {
#             "from": account.address,
#             "to": recipient,
#             "value": amount
#         }
#     )

#     return {
#         "chainId": 555,
#         "from": account.address,
#         "to": recipient,
#         "value": amount,
#         "gasPrice": w3.eth.gasPrice,
#         "gas": gasEstimate,
#         "nonce": w3.eth.getTransactionCount(account.address)
#     }
# # # Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.


# def send_tx(account, recipient, amount):
#     tx = create_tx(
#         account,
#         recipient,
#         amount
#     )
#     sign_tx = account.sign_transaction(tx)
#     result = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
#     print(f"This is my hash number: {result.hex()}")

#     return result.hex()
