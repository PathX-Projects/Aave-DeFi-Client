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

"""Get the current debt payable from the Aave client"""
total_borrowing_power, total_debt = aave_client_kovan.get_user_data(lending_pool_contract)
print(f"Total Outstanding Debt (in ETH): {total_debt:.18f}")

"""Repay a percentage of debt payable with DAI"""
REPAY_PERCENTAGE = 0.50  # Repay 50% of debts using DAI
debt_asset = aave_client_kovan.get_reserve_token("DAI")  # Get the ReserveToken object for the underlying asset (DAI)
transaction_hash = aave_client_kovan.repay_percentage(lending_pool_contract=lending_pool_contract,
                                                      repay_percentage=REPAY_PERCENTAGE, repay_asset=debt_asset)
print(transaction_hash)
