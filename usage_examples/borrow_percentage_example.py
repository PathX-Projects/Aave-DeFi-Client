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

    """Get the current borrowing power from the Aave client"""
    borrowable, debt, collateral = aave_client_goerli.get_user_data()
    print(f"Total Borrowing Power (in ETH): {borrowable:.18f}")

    """Borrow DAI as a percentage of borrowing power"""
    borrow_token = aave_client_goerli.get_reserve_token("DAI")  # Get the ReserveToken object for our underlying asset (DAI)
    borrow_percentage = 0.95  # Borrow DAI using 95% of borrowing power
    tx_hash = aave_client_goerli.borrow_percentage(borrow_percentage=borrow_percentage,
                                                   borrow_asset=borrow_token)
    print("Transaction Hash:", tx_hash)
