import os  # For fetching environment variables
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aave_python import AaveStakingClient

"""Obstantiate the client using the Kovan testnet"""
aave_client_kovan = AaveStakingClient(WALLET_ADDRESS=os.getenv('WALLET_ADDRESS'),
                                      PRIVATE_WALLET_KEY=os.getenv('PRIVATE_WALLET_KEY'),
                                      KOVAN_RPC_URL=os.getenv("KOVAN_RPC_URL"),
                                      GAS_STRATEGY="medium")  # see the __init__ function for available gas strategies
"""Obstantiate the client using the Ethereum Mainnet"""
# aave_client_mainnet = AaveStakingClient(WALLET_ADDRESS=os.getenv('WALLET_ADDRESS'),
#                                         PRIVATE_WALLET_KEY=os.getenv('PRIVATE_WALLET_KEY'),
#                                         MAINNET_RPC_URL=os.getenv('MAINNET_RPC_URL'),
#                                         GAS_STRATEGY="medium")

"""Obstantiate the instance of the Aave lending pool smart contract"""
lending_pool_contract = aave_client_kovan.get_lending_pool()

"""Get the ReserveToken object for the desired underlying asset to withdraw"""
withdraw_token = aave_client_kovan.get_reserve_token(symbol="WETH")

"""Withdraw tokens"""
WITHDRAW_AMOUNT = 0.0001  # As in 0.0001 WETH to be withdrawn from Aave
withdraw_transaction_receipt = aave_client_kovan.withdraw(withdraw_token=withdraw_token, withdraw_amount=WITHDRAW_AMOUNT,
                                                          lending_pool_contract=lending_pool_contract)
print("AaveTrade Object:", withdraw_transaction_receipt)