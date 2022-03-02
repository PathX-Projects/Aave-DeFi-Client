import os  # For fetching environment variables
from aave_client import AaveStakingClient

"""REPLACE THESE VALUES WITH YOUR CREDENTIALS OR STORE THE ENVIRONMENT VARIABLES"""
PUBLIC_WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
PRIVATE_WALLET_KEY = os.getenv('PRIVATE_WALLET_KEY')
KOVAN_RPC_URL = os.getenv("KOVAN_RPC_URL")
ETH_TO_CONVERT = 0.0001

"""Obstantiate the client using the Kovan testnet"""
aave_client_kovan = AaveStakingClient(WALLET_ADDRESS=PUBLIC_WALLET_ADDRESS,
                                      PRIVATE_WALLET_KEY=PRIVATE_WALLET_KEY,
                                      KOVAN_RPC_URL=KOVAN_RPC_URL)

"""Run the conversion function to turn testnet ETH into erc20 WETH"""
transaction_hash = aave_client_kovan.convert_eth_to_weth(amount_in_eth=ETH_TO_CONVERT)
print("Converted ETH to WETH. Transaction Hash:", transaction_hash)