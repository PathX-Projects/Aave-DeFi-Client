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

"""Get the current borrowing power from the Aave client"""
borrowable, debt, collateral = aave_client_kovan.get_user_data(lending_pool_contract)
print(f"Total Borrowing Power (in ETH): {borrowable:.18f}")

"""Borrow DAI as a percentage of borrowing power"""
borrow_token = aave_client_kovan.get_reserve_token("DAI")  # Get the ReserveToken object for our underlying asset (DAI)
borrow_percentage = 0.95  # Borrow DAI using 95% of borrowing power
tx_hash = aave_client_kovan.borrow_percentage(lending_pool_contract=lending_pool_contract,
                                              borrow_percentage=borrow_percentage,
                                              borrow_asset=borrow_token)
print("Transaction Hash:", tx_hash)
