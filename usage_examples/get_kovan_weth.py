import os  # For fetching environment variables
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aave_python import AaveClient

""" OUTDATED """
if __name__ == "__main__":
    """REPLACE THESE VALUES WITH YOUR CREDENTIALS OR STORE THE ENVIRONMENT VARIABLES"""
    PUBLIC_WALLET_ADDRESS = os.getenv('wallet_address')
    PRIVATE_WALLET_KEY = os.getenv('private_wallet_key')
    KOVAN_RPC_URL = os.getenv("goerli_rpc_url")
    ETH_TO_CONVERT = 0.0001

    """Obstantiate the client using the Kovan testnet"""
    aave_client_kovan = AaveClient(wallet_address=PUBLIC_WALLET_ADDRESS,
                                   private_wallet_key=PRIVATE_WALLET_KEY,
                                   goerli_rpc_url=KOVAN_RPC_URL)

    """Run the conversion function to turn testnet ETH into erc20 WETH"""
    transaction_hash = aave_client_kovan.convert_eth_to_weth(amount_in_eth=ETH_TO_CONVERT)
    print("Converted ETH to WETH. Transaction Hash:", transaction_hash)