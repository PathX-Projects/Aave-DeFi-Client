from dotenv import load_dotenv
load_dotenv()

import os  # For fetching environment variables
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aave_python import AaveStakingClient


"""Obstantiate the client using the Kovan testnet"""
# aave_client = AaveStakingClient(WALLET_ADDRESS=os.getenv('WALLET_ADDRESS'),
#                                       PRIVATE_WALLET_KEY=os.getenv('PRIVATE_WALLET_KEY'),
#                                       KOVAN_RPC_URL=os.getenv("KOVAN_RPC_URL"),
#                                       GAS_STRATEGY="medium")  # see the __init__ function for available gas strategies

"""Obstantiate the client using the Ethereum Mainnet"""
aave_client = AaveStakingClient(WALLET_ADDRESS=os.getenv('WALLET_ADDRESS'),
                                PRIVATE_WALLET_KEY=os.getenv('PRIVATE_WALLET_KEY'),
                                MAINNET_RPC_URL=os.getenv('MAINNET_RPC_URL'),
                                GAS_STRATEGY="medium")

"""Obstantiate the instance of the Aave lending pool smart contract"""
lending_pool_contract = aave_client.get_lending_pool()

"""Get the current borrowing power from the Aave client"""
print(aave_client.get_user_data(lending_pool_contract))

print(aave_client.get_asset_price("0x4Fabb145d64652a948d72533023f6E7A623C7C53"))