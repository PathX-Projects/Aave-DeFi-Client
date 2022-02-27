import os  # For fetching environment variables
from aave_client import AaveStakingClient

# Initialize Client:
aave_client = AaveStakingClient(WALLET_ADDRESS=os.getenv('WALLET_ADDRESS'),
                                PRIVATE_WALLET_KEY=os.getenv('PRIVATE_WALLET_KEY'),
                                KOVAN_RPC_URL=os.getenv("KOVAN_RPC_URL"),
                                GAS_STRATEGY="medium")

# Get the lending pool smart contract:
lending_pool = aave_client.get_lending_pool()

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
# token = aave_client.get_reserve_token("WETH")
# amount = 1.2
# print(f"{token.symbol} Decimal Units Amount:", int(amount * (10 ** int(token.decimals))))
# So, 1.2 USDC will be 1.2 * 10 ^ 6