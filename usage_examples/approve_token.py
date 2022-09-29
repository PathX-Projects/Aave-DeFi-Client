import os  # For fetching environment variables
import sys
from dotenv import load_dotenv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
load_dotenv()

from aave_python import AaveClient
from web3.constants import MAX_INT


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

    """Get ReserveToken object"""
    token = aave_client_goerli.get_reserve_token('DAI')

    """Approve Token"""
    txn, gas_spend = aave_client_goerli.approve_erc20(erc20_address=token.address,
                                                      amount_in_decimal_units=int(MAX_INT, 16))
    print(txn, gas_spend)
