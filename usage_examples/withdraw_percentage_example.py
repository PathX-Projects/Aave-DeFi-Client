import os  # For fetching environment variables
from aave_client import AaveStakingClient

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
WITHDRAW_PERCENTAGE = 0.50  # As in you'd like to withdraw WETH amounting to 50% of the total available.
withdraw_transaction_receipt = aave_client_kovan.withdraw_percentage(withdraw_token=withdraw_token,
                                                                     withdraw_percentage=WITHDRAW_PERCENTAGE,
                                                                     lending_pool_contract=lending_pool_contract)
print("AaveTrade Object:", withdraw_transaction_receipt)
