import os  # For fetching environment variables
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aave_python import AaveClient


if __name__ == "__main__":
    """Obstantiate the client using the Goerli testnet"""
    aave_client_goerli = AaveClient(wallet_address=os.getenv('wallet_address'),
                                    private_wallet_key=os.getenv('private_wallet_key'),
                                    goerli_rpc_url=os.getenv("goerli_rpc_url"),
                                    gas_strategy="medium")  # see the __init__ function for available gas strategies
    """Obstantiate the client using the Ethereum Mainnet"""
    # aave_client_mainnet = AaveClient(wallet_address=os.getenv('wallet_address'),
    #                                         private_wallet_key=os.getenv('private_wallet_key'),
    #                                         mainnet_rpc_url=os.getenv('mainnet_rpc_url'),
    #                                         gas_strategy="medium")

    """Get the current debt payable from the Aave client"""
    total_borrowing_power, total_debt = aave_client_goerli.get_user_data()
    print(f"Total Outstanding Debt (in ETH): {total_debt:.18f}")

    """Repay a percentage of debt payable with DAI"""
    REPAY_PERCENTAGE = 0.50  # Repay 50% of debts using DAI
    debt_asset = aave_client_goerli.get_reserve_token("DAI")  # Get the ReserveToken object for the underlying asset (DAI)
    transaction_hash = aave_client_goerli.repay_percentage(repay_percentage=REPAY_PERCENTAGE, repay_asset=debt_asset)
    print(transaction_hash)
