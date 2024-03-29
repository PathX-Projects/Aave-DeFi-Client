import datetime
import os  # For fetching environment variables
import time
from pprint import pprint
from aave_python import AaveClient

# Initialize Client:
aave_client = AaveClient(wallet_address=os.getenv('wallet_address'),
                         private_wallet_key=os.getenv('private_wallet_key'),
                         goerli_rpc_url=os.getenv("goerli_rpc_url"),
                         gas_strategy="medium")

# Get the lending pool smart contract:
lending_pool = aave_client._get_lending_pool()

""" ------------------------------------------- Testing Cases ------------------------------------------------ """
# Convert ETH to WEI:
run_test = False
if run_test:
    convert_amount = 0.001
    aave_client.convert_eth_to_weth(amount_in_eth=convert_amount)

# Deposit Tokens:
run_test = False
if run_test:
    deposit_token = aave_client.get_reserve_token(symbol="WETH")
    # deposit_amount =
    # # First you must approve the transaction:
    # print(aave_client.approve_erc20(erc20_address=deposit_token.address,
    #                                 lending_pool_contract=lending_pool,
    #                                 amount_in_decimal_units=depo_amnt).hex())
    # print("Approved in", time.time() - approval_start, "seconds")
    # deposit_hash = aave_client.deposit_to_aave(deposit_token_erc20_address=weth_token_addr, amount_in_wei=depo_amnt,
    #                                            lending_pool_contract=lending_pool)

# Miscellaneous Test Cases:
token = aave_client.get_reserve_token("WETH")
amount = 1.2
print(f"{token.symbol} Decimal Units Amount:", int(amount * (10 ** int(token.decimals))))

borrow_token = aave_client.get_reserve_token("USDC")
borrow_percentage = 1.0
total_borrowable_in_eth, total_debt_eth, total_collateral_eth = aave_client.get_user_data(lending_pool)
print("Borrowable (ETH):", total_borrowable_in_eth, "Debt (ETH):", total_debt_eth, "Collateral (ETH):", total_collateral_eth)
weth_to_borrow_asset = aave_client.get_asset_price(base_address=token.address, quote_address=borrow_token.address)
print(weth_to_borrow_asset)
amount_to_borrow = weth_to_borrow_asset * (total_borrowable_in_eth * borrow_percentage)
print("\nAmount to borrow:", amount_to_borrow, borrow_token.symbol)
print(f"\nOutstanding Debt (in ETH): {total_debt_eth:.18f} ({total_debt_eth * weth_to_borrow_asset} DAI)")

pprint(aave_client.list_reserve_tokens())
# So, 1.2 USDC will be 1.2 * 10 ^ 6