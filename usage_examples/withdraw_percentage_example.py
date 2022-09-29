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

    """Get the ReserveToken object for the desired underlying asset to withdraw"""
    withdraw_token = aave_client_goerli.get_reserve_token(symbol="WETH")

    """Withdraw tokens"""
    WITHDRAW_PERCENTAGE = 0.50  # As in you'd like to withdraw WETH amounting to 50% of the total available.
    withdraw_transaction_receipt = aave_client_goerli.withdraw_percentage(withdraw_token=withdraw_token,
                                                                          withdraw_percentage=WITHDRAW_PERCENTAGE)
    print("AaveTrade Object:", withdraw_transaction_receipt)
