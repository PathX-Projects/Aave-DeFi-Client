from dotenv import load_dotenv
load_dotenv()

import os  # For fetching environment variables
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aave_python import AaveClient


if __name__ == "__main__":
    """Obstantiate the client using the Goerli testnet"""
    # aave_client = AaveClient(wallet_address=os.getenv('wallet_address'),
    #                                 private_wallet_key=os.getenv('private_wallet_key'),
    #                                 goerli_rpc_url=os.getenv("goerli_rpc_url"),
    #                                 gas_strategy="medium")  # see the __init__ function for available gas strategies

    """Obstantiate the client using the Ethereum Mainnet"""
    aave_client = AaveClient(wallet_address=os.getenv('WALLET_ADDRESS'),
                             private_wallet_key=os.getenv('PRIVATE_WALLET_KEY'),
                             mainnet_rpc_url=os.getenv('MAINNET_RPC_URL'),
                             gas_strategy="medium")

    """Get the current borrowing power from the Aave client"""
    print(aave_client.get_user_data())

    print(aave_client.get_asset_price("0x4Fabb145d64652a948d72533023f6E7A623C7C53"))

    """ Get all tokens with debts from the Aave client"""
    print(aave_client.get_all_reserve_balances(hide_empty_assets=True))