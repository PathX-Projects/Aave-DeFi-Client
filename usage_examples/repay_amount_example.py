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

"""Choose the asset that you want to repay (in this case, DAI)"""
DAI_token = aave_client_kovan.get_reserve_token("DAI")

"""Get the current debt payable from the Aave client and convert it from ETH to the target asset"""
total_borrowing_power, total_debt_in_eth = aave_client_kovan.get_user_data(lending_pool_contract)
weth_to_repay_asset = aave_client_kovan.get_asset_price(base_address=aave_client_kovan.get_reserve_token("WETH").address,
                                                        quote_address=DAI_token.address)
total_debt_in_DAI = weth_to_repay_asset * total_debt_in_eth
print(f"Total Outstanding Debt: {total_debt_in_DAI:.18f} DAI")

"""Repay debts"""
AMOUNT_TO_REPAY = 0.5  # Repay 0.5 DAI of the current outstanding debt
transaction_hash = aave_client_kovan.repay(lending_pool_contract=lending_pool_contract, repay_amount=AMOUNT_TO_REPAY,
                                           repay_asset=DAI_token)
print("Transaction Hash:", transaction_hash)