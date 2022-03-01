from aave_client import AaveStakingClient

"""Obstantiate the client"""
aave_client = AaveStakingClient()

"""Deposit Collateral Example"""
deposit_token = aave_client.get_reserve_token(symbol="WETH")
# deposit_amount =
# # First you must approve the transaction:
# print(aave_client.approve_erc20(erc20_address=deposit_token.address,
#                                 lending_pool_contract=lending_pool,
#                                 amount_in_decimal_units=depo_amnt).hex())
# print("Approved in", time.time() - approval_start, "seconds")
# deposit_hash = aave_client.deposit_to_aave(deposit_token_erc20_address=weth_token_addr, amount_in_wei=depo_amnt,
#                                            lending_pool_contract=lending_pool)