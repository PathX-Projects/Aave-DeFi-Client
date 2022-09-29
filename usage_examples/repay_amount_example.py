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

    """Choose the asset that you want to repay (in this case, DAI)"""
    DAI_token = aave_client_goerli.get_reserve_token("DAI")

    """Get the current debt payable from the Aave client and convert it from ETH to the target asset"""
    total_borrowing_power, total_debt_in_eth = aave_client_goerli.get_user_data()
    weth_to_repay_asset = aave_client_goerli.get_asset_price(base_address=aave_client_goerli.get_reserve_token("WETH").address,
                                                             quote_address=DAI_token.address)
    total_debt_in_DAI = weth_to_repay_asset * total_debt_in_eth
    print(f"Total Outstanding Debt: {total_debt_in_DAI:.18f} DAI")

    """Repay debts"""
    AMOUNT_TO_REPAY = 0.5  # Repay 0.5 DAI of the current outstanding debt
    transaction_hash = aave_client_goerli.repay(repay_amount=AMOUNT_TO_REPAY, repay_asset=DAI_token)
    print("Transaction Hash:", transaction_hash)