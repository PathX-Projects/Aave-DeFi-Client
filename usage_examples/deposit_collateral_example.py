import os  # For fetching environment variables
import sys
from dotenv import load_dotenv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
load_dotenv()

from aave_python import AaveClient


if __name__ == "__main__":
    """Obstantiate the client using the Goerli testnet"""
    # aave_client = AaveClient(wallet_address=os.getenv('wallet_address'),
    #                                 private_wallet_key=os.getenv('private_wallet_key'),
    #                                 goerli_rpc_url=os.getenv("goerli_rpc_url"),
    #                                 gas_strategy="medium")  # see the __init__ function for available gas strategies
    """Obstantiate the client using the Ethereum Mainnet"""
    aave_client = AaveClient(wallet_address=os.getenv('wallet_address'),
                             private_wallet_key=os.getenv('private_wallet_key'),
                             mainnet_rpc_url=os.getenv('mainnet_rpc_url'),
                             gas_strategy="medium")

    """Get the ReserveToken object for the desired underlying asset to deposit"""
    deposit_token = aave_client.get_reserve_token(symbol="USDT")

    """Deposit tokens"""
    DEPOSIT_AMOUNT = 4  # As in 4.0 USDT to be deposited
    deposit_hash = aave_client.deposit(deposit_token=deposit_token, deposit_amount=DEPOSIT_AMOUNT)
    print("Transaction Hash:", deposit_hash)