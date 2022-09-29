from pprint import pprint
import json
import os
import time
from datetime import datetime
from dataclasses import dataclass
import concurrent.futures

from .abi import ABIReference
from .models import ReserveToken, AaveTrade
from .network_configs import *

import requests
import web3.eth
from web3 import Web3
from web3.gas_strategies.time_based import *


"""------------------------------------------ MAIN AAVE STAKING CLIENT ----------------------------------------------"""
class AaveClient:
    """Fully plug-and-play AAVE staking client in Python3"""
    def __init__(self, wallet_address: str, private_wallet_key: str,
                 mainnet_rpc_url: str = None, goerli_rpc_url: str = None,
                 gas_strategy: str = "medium", web3_instance: Web3 = None):
        assert wallet_address is not None, "Wallet address is None - Required for instantiation"
        assert private_wallet_key is not None, "Private wallet key is None - Required for instantiation"

        self.private_key = private_wallet_key
        self.wallet_address = Web3.toChecksumAddress(wallet_address)

        if goerli_rpc_url is None and mainnet_rpc_url is None:
            raise Exception("Missing RPC URLs for all available choices. Must use at least one network configuration.")
        elif goerli_rpc_url is not None and mainnet_rpc_url is not None:
            raise Exception("Only one active network supported at a time. Please use either the Goerli testnet or Mainnet network.")
        else:
            self.active_network = GoerliConfig(goerli_rpc_url) if goerli_rpc_url is not None else MainnetConfig(
                mainnet_rpc_url)

        self.w3 = self._connect() if web3_instance is None else web3_instance

        # Set protocol data provider
        self.data_provider_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(self.active_network.protocol_data_provider),
            abi=ABIReference.protocol_data_provider
        )

        # Set the lending pool provider
        self.lending_pool_contract = self._get_lending_pool()

        # Populate active network with reserve tokens if needed
        if len(self.active_network.aave_tokens) == 0:
            self._store_reserve_tokens()

        # Gas strategies
        if gas_strategy.lower() == "fast":
            """Transaction mined within 60 seconds."""
            self.w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
            self.timeout = 60
        elif gas_strategy.lower() == "medium":
            """Transaction mined within 5 minutes."""
            self.w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
            self.timeout = 60 * 5
        elif gas_strategy.lower() == "slow":
            """Transaction mined within 1 hour."""
            self.w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
            self.timeout = 60 * 60
        elif gas_strategy.lower() == "glacial":
            """Transaction mined within 24 hours."""
            self.w3.eth.setGasPriceStrategy(glacial_gas_price_strategy)
            self.timeout = 60 * 1440
        else:
            raise ValueError("Invalid gas strategy. Available gas strategies are 'fast', 'medium', 'slow', or 'glacial'")

    def _connect(self) -> Web3:
        try:
            return Web3(Web3.HTTPProvider(self.active_network.rpc_url))
        except:
            raise ConnectionError(f"Could not connect to {self.active_network.net_name} network with RPC URL: "
                                  f"{self.active_network.rpc_url}")

    def process_transaction_receipt(self, tx_hash: web3.eth.HexBytes, asset_amount: float,
                                    reserve_token: ReserveToken, operation: str, interest_rate_mode: str = None,
                                    approval_gas_cost: float = 0) -> AaveTrade:
        print(f"Awaiting transaction receipt for transaction hash: {tx_hash.hex()} (timeout = {self.timeout} seconds)")
        receipt = dict(self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=self.timeout))

        verification_timestamp = datetime.utcnow()
        gas_fee = Web3.fromWei(int(receipt['effectiveGasPrice']) * int(receipt['gasUsed']), 'ether') + approval_gas_cost

        return AaveTrade(hash=tx_hash.hex(),
                         timestamp=int(datetime.timestamp(verification_timestamp)),
                         datetime=verification_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                         contract_address=receipt['contractAddress'],
                         from_address=receipt['from'],
                         to_address=receipt['to'],
                         gas_price=gas_fee,
                         asset_symbol=reserve_token.symbol, asset_address=reserve_token.address,
                         asset_amount=asset_amount,
                         asset_amount_decimal_units=self.convert_to_decimal_units(reserve_token, asset_amount),
                         interest_rate_mode=interest_rate_mode, operation=operation)

    def convert_eth_to_weth(self, amount_in_eth: float) -> AaveTrade:
        """Mints WETH by depositing ETH, then returns the transaction hash string"""
        print(f"Converting {amount_in_eth} ETH to WETH...")
        amount_in_wei = Web3.toWei(amount_in_eth, 'ether')
        nonce = self.w3.eth.getTransactionCount(self.wallet_address)
        weth_address = Web3.toChecksumAddress(self.active_network.weth_token)
        weth = self.w3.eth.contract(address=weth_address, abi=ABIReference.weth_abi)
        function_call = weth.functions.deposit()
        transaction = function_call.buildTransaction(
            {
                "chainId": self.active_network.chain_id,
                "from": self.wallet_address,
                "nonce": nonce,
                # "value": Web3.toWei(amount_in_decimal_units, 'ether'),
                "value": amount_in_wei
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.process_transaction_receipt(tx_hash, asset_amount=amount_in_eth,
                                                   reserve_token=self.get_reserve_token("WETH"),
                                                   operation="Convert ETH to WETH")
        print("Received WETH!")
        return receipt

    def _get_lending_pool(self) -> web3.eth.Contract:
        try:
            lending_pool_addresses_provider_address = Web3.toChecksumAddress(
                self.active_network.lending_pool_addresses_provider
            )
            lending_poll_addresses_provider = self.w3.eth.contract(
                address=lending_pool_addresses_provider_address,
                abi=ABIReference.lending_pool_addresses_provider_abi,
            )
            lending_pool_address = (
                lending_poll_addresses_provider.functions.getLendingPool().call()
            )
            lending_pool = self.w3.eth.contract(
                address=lending_pool_address, abi=ABIReference.lending_pool_abi)
            return lending_pool
        except Exception as exc:
            raise Exception(f"Could not fetch the Aave lending pool smart contract - Error: {exc}")

    def approve_erc20(self, erc20_address: str, amount_in_decimal_units: int,
                      nonce: int =None, force: bool = False) -> tuple:
        """
        Approve the smart contract to take the tokens out of the wallet

        Returns a tuple of the following:
            if force is True or allowance < amount_in_decimal_units:
                (transaction hash string, approval gas cost)
            else:
                (None, 0)
        """
        nonce = nonce if nonce else self.w3.eth.getTransactionCount(self.wallet_address)

        erc20_address = Web3.toChecksumAddress(erc20_address)
        erc20 = self.w3.eth.contract(address=erc20_address, abi=ABIReference.erc20_abi)
        if not force:
            if erc20.functions.allowance(self.wallet_address, self.lending_pool_contract.address).call() >= amount_in_decimal_units:
                return None, 0

        lending_pool_address = Web3.toChecksumAddress(self.lending_pool_contract.address)
        function_call = erc20.functions.approve(lending_pool_address, amount_in_decimal_units)
        transaction = function_call.buildTransaction(
            {
                "chainId": self.active_network.chain_id,
                "from": self.wallet_address,
                "nonce": nonce,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = dict(self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=self.timeout))

        print(f"Approved {amount_in_decimal_units} of {erc20_address} for contract {lending_pool_address}")
        return tx_hash.hex(), Web3.fromWei(int(receipt['effectiveGasPrice']) * int(receipt['gasUsed']), 'ether')

    def withdraw(self, withdraw_token: ReserveToken, withdraw_amount: float, nonce=None) -> AaveTrade:
        """
        Withdraws the amount of the withdraw_token from Aave, and burns the corresponding aToken.

        Parameters:
            withdraw_token: The ReserveToken object of the token to be withdrawn from Aave.

            withdraw_amount:  The amount of the 'withdraw_token' to withdraw from Aave (e.g. 0.001 WETH)

            nonce: Manually specify the transaction count/ID. Leave as None to get the current transaction count from
                   the user's wallet set at self.wallet_address.

        Returns:
            The AaveTrade object - See ./models.py

        Smart Contract Reference:
            https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#withdraw
        """
        nonce = nonce if nonce else self.w3.eth.getTransactionCount(self.wallet_address)
        amount_in_decimal_units = self.convert_to_decimal_units(withdraw_token, withdraw_amount)

        # First, attempt to approve the transaction:
        print(f"Approving transaction to withdraw {withdraw_amount:.{withdraw_token.decimals}f} of {withdraw_token.symbol} from Aave...")
        try:
            approval_hash, approval_gas = self.approve_erc20(erc20_address=withdraw_token.address,
                                                             amount_in_decimal_units=amount_in_decimal_units,
                                                             nonce=nonce)
        except Exception as exc:
            raise UserWarning(f"Could not approve withdraw transaction - Error Code {exc}")

        # Second, if the transaction is approved, create the transaction to deposit the tokens to Aave:
        print(f"Withdrawing {withdraw_amount} of {withdraw_token.symbol} from Aave...")
        function_call = self.lending_pool_contract.functions.withdraw(withdraw_token.address,
                                                                      amount_in_decimal_units,
                                                                      self.wallet_address)
        transaction = function_call.buildTransaction(
            {
                "chainId": self.active_network.chain_id,
                "from": self.wallet_address,
                "nonce": nonce + 1 if approval_hash else nonce,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.process_transaction_receipt(tx_hash, withdraw_amount, withdraw_token,
                                                   operation="Withdraw", approval_gas_cost=approval_gas)
        # receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=self.timeout)
        print(f"Successfully withdrew {withdraw_amount:.{withdraw_token.decimals}f} of {withdraw_token.symbol} from Aave")
        return receipt

    def withdraw_percentage(self, withdraw_token: ReserveToken, withdraw_percentage: float, nonce=None) -> AaveTrade:
        """Same parameters as the self.withdraw() function, except instead of 'withdraw_amount', you will pass the
        percentage of total available collateral on Aave that you would like to withdraw from in the 'withdraw_percentage'
        parameter in the following format: 0.0 (0% of borrowing power) to 1.0 (100% of borrowing power)"""

        if withdraw_percentage > 1.0:
            raise ValueError("Cannot withdraw more than 100% of available collateral of Aave. "
                             "Please pass a value between 0.0 and 1.0")

        # Calculate withdraw amount by multiplying the total collateral on Aave by the withdraw_percentage parameter.
        total_collateral = self.get_user_data()[2]
        weth_to_withdraw_asset = self.get_asset_price(base_address=self.get_reserve_token("WETH").address,
                                                      quote_address=withdraw_token.address)
        withdraw_amount = weth_to_withdraw_asset * (total_collateral * withdraw_percentage)

        return self.withdraw(withdraw_token, withdraw_amount, nonce)

    def deposit(self, deposit_token: ReserveToken, deposit_amount: float, nonce=None) -> AaveTrade:
        """
        Deposits the 'deposit_amount' of the 'deposit_token' to Aave collateral.

        Parameters:
            deposit_token: The ReserveToken object of the token to be deposited/collateralized on Aave

            deposit_amount: The amount of the 'deposit_token' to deposit on Aave (e.g. 0.001 WETH)

            nonce: Manually specify the transaction count/ID. Leave as None to get the current transaction count from
                   the user's wallet set at self.wallet_address.

        Returns:
            The AaveTrade object - See ./models.py

        Smart Contract Reference:
            https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#deposit
        """

        nonce = nonce if nonce else self.w3.eth.getTransactionCount(self.wallet_address)

        amount_in_decimal_units = self.convert_to_decimal_units(deposit_token, deposit_amount)

        # First, attempt to approve the transaction:
        print(f"Approving transaction to deposit {deposit_amount} of {deposit_token.symbol} to Aave...")
        try:
            approval_hash, approval_gas = self.approve_erc20(erc20_address=deposit_token.address,
                                                             amount_in_decimal_units=amount_in_decimal_units,
                                                             nonce=nonce)
        except Exception as exc:
            raise UserWarning(f"Could not approve deposit transaction - Error Code {exc}")

        # Second, if the transaction is approved, create the transaction to deposit the tokens to Aave:
        print(f"Depositing {deposit_amount} of {deposit_token.symbol} to Aave...")
        function_call = self.lending_pool_contract.functions.deposit(deposit_token.address,
                                                                amount_in_decimal_units,
                                                                self.wallet_address,
                                                                0)  # The 0 is deprecated and must persist
        transaction = function_call.buildTransaction(
            {
                "chainId": self.active_network.chain_id,
                "from": self.wallet_address,
                "nonce": nonce + 1 if approval_hash else nonce,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.process_transaction_receipt(tx_hash, deposit_amount, deposit_token,
                                                   operation="Deposit", approval_gas_cost=approval_gas)
        # receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=self.timeout)
        print(f"Successfully deposited {deposit_amount} of {deposit_token.symbol}")
        return receipt

    def get_user_data(self, in_wei=True) -> tuple:
        """
        - Fetches user account data (shown below) across all reserves
        - Only returns the borrowing power (in ETH), and the total user debt (in ETH)

        Parameters:
            in_wei: If True, returns the collateral, debt, and borrows values in wei instead of the token

        Returns:
            totalCollateralETH: total collateral in ETH of the use (wei decimal unit)
            totalDebtETH: total debt in ETH of the user (wei decimal unit)
            availableBorrowsETH: borrowing power left of the user (wei decimal unit)
            currentLiquidationThreshold: liquidation threshold of the user (1e4 format => percentage plus two decimals)
            ltv: Loan To Value of the user (1e4 format => percentage plus two decimals)
            healthFactor: current health factor of the user.

        https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#getuseraccountdata
        """
        user_data = self.lending_pool_contract.functions.getUserAccountData(self.wallet_address).call()
        try:
            (
                total_collateral_eth,  # total collateral in ETH of the use (wei decimal unit)
                total_debt_eth,  # total debt in ETH of the user (wei decimal unit)
                available_borrow_eth,  # borrowing power left of the user (wei decimal unit)
                liquidation_threshold,
                # liquidation threshold of the user (1e4 format => percentage plus two decimals)
                ltv,  # Loan To Value of the user (1e4 format => percentage plus two decimals)
                health_factor,  # current health factor of the user
            ) = user_data
        except TypeError:
            raise Exception(f"Could not unpack user data due to a TypeError - Received: {user_data}")

        """
        Health Factor =
        (total_collateral_ETH * (liquidation_threshold / 1e4)) / total_debt_eth
        """

        if not in_wei:
            available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
            total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
            total_debt_eth = Web3.fromWei(total_debt_eth, "ether")

        return available_borrow_eth, total_debt_eth, total_collateral_eth, \
            liquidation_threshold, ltv, health_factor

    def get_asset_price(self, base_address: str, quote_address: str = None) -> float:
        """
        If quote_address is None, returns the asset price in Ether
        If quote_address is not None, returns the pair price of BASE/QUOTE

        https://docs.aave.com/developers/v/2.0/the-core-protocol/price-oracle#getassetprice
        """

        # For calling Chainlink price feeds (Deprecated):
        # link_eth_address = Web3.toChecksumAddress(self.active_network.link_eth_price_feed)
        # link_eth_price_feed = self.w3.eth.contract(
        #     address=link_eth_address, abi=ABIReference.price_feed_abi)
        # latest_price = Web3.fromWei(link_eth_price_feed.functions.latestRoundData().call()[1], "ether")
        # print(f"The LINK/ETH price is {latest_price}")

        # For calling the Aave price oracle:
        price_oracle_address = self.w3.eth.contract(
            address=Web3.toChecksumAddress(self.active_network.lending_pool_addresses_provider),
            abi=ABIReference.lending_pool_addresses_provider_abi,
        ).functions.getPriceOracle().call()

        price_oracle_contract = self.w3.eth.contract(
            address=price_oracle_address, abi=ABIReference.aave_price_oracle_abi
        )

        latest_price = Web3.fromWei(int(price_oracle_contract.functions.getAssetPrice(base_address).call()),
                                    'ether')
        if quote_address is not None:
            quote_price = Web3.fromWei(int(price_oracle_contract.functions.getAssetPrice(quote_address).call()),
                                       'ether')
            latest_price = latest_price / quote_price
        return float(latest_price)

    def get_user_reserve_data(self, reserve_token: ReserveToken) -> tuple:
        """
        :param reserve_token: The ReserveToken object for the desired reserve token to fetch data

        :returns: tuple
            - currentATokenBalance (int)
            - currentStableDebt (int)
            - currentVariableDebt (int)
            - principalStableDebt (int)
            - scaledVariableDebt (int)
            - stableBorrowRate (int)
            - liqidityRate (int)
            - stableRateLastUpdated (int)
            - usageAsCollateralEnabled (bool)
        """
        return self.data_provider_contract.functions.getUserReserveData(reserve_token.address, self.wallet_address).call()

    def get_all_reserves_tokens(self) -> list[ReserveToken]:
        # Get the list of reserves token symbols:
        reserves_tokens = [t[0].upper() for t in self.data_provider_contract.functions.getAllReservesTokens().call()]

        # Pull tokens from active networks tokenlist URL and prepare output
        output = []
        for token in requests.get(self.active_network.aave_tokenlist_url).json()['proto']:
            if token['symbol'].upper() in reserves_tokens:
                output.append(ReserveToken(**token))
        return output

    def borrow(self, borrow_asset: ReserveToken, borrow_amount: float,
               nonce=None, interest_rate_mode: str = "stable") -> AaveTrade:
        """
        Borrows the underlying asset (erc20_address) as long as the amount is within the confines of
        the user's buying power.

        Parameters:
            borrow_asset: The ReserveToken which you want to borrow from Aave. To get the reserve token, you can use the
                          self.get_reserve_token(symbol: str) function.
            borrow_amount: Amount of the underlying asset to borrow. The amount should be measured in the asset's
                           currency (e.g. for ETH, borrow_amount=0.05, as in 0.05 ETH)
            nonce: Manually specify the transaction count/ID. Leave as None to get the current transaction count from
                   the user's wallet set at self.wallet_address.
            interest_rate_mode: The type of Aave interest rate mode for borrow debt, with the options being a 'stable'
                                or 'variable' interest rate.

        Returns:
            The AaveTrade object - See line 52 for datapoints reference

        Smart Contract Docs:
        https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#borrow
        """

        rate_mode_str = interest_rate_mode
        if interest_rate_mode.lower() == "stable":
            interest_rate_mode = 1
        elif interest_rate_mode.lower() == "variable":
            interest_rate_mode = 0
        else:
            raise ValueError(f"Invalid interest rate mode passed to the borrow_erc20 function ({interest_rate_mode}) - "
                             f"Valid interest rate modes are 'stable' and 'variable'")

        # Calculate amount to borrow in decimal units:
        borrow_amount_in_decimal_units = self.convert_to_decimal_units(borrow_asset, borrow_amount)

        # Create and send transaction to borrow assets against collateral:
        print(f"\nCreating transaction to borrow {borrow_amount:.{borrow_asset.decimals}f} {borrow_asset.symbol}...")
        function_call = self.lending_pool_contract.functions.borrow(Web3.toChecksumAddress(borrow_asset.address),
                                                                    borrow_amount_in_decimal_units,
                                                                    interest_rate_mode, 0,  # 0 must not be changed, it is deprecated
                                                                    self.wallet_address)
        transaction = function_call.buildTransaction(
            {
                "chainId": self.active_network.chain_id,
                "from": self.wallet_address,
                "nonce": nonce if nonce else self.w3.eth.getTransactionCount(self.wallet_address),
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.process_transaction_receipt(tx_hash, borrow_amount, borrow_asset, operation="Borrow",
                                                   interest_rate_mode=rate_mode_str)

        print(f"\nBorrowed {borrow_amount:.{borrow_asset.decimals}f} of {borrow_asset.symbol}")
        print(f"Remaining Borrowing Power: {self.get_user_data()[0]:.18f}")
        print(f"Transaction Hash: {tx_hash.hex()}")
        return receipt

    def convert_to_decimal_units(self, reserve_token: ReserveToken, token_amount: float) -> int:
        """integer units i.e amt * 10 ^ (decimal units of the token). So, 1.2 USDC will be 1.2 * 10 ^ 6"""
        return int(token_amount * (10 ** int(reserve_token.decimals)))

    def borrow_percentage(self, borrow_percentage: float, borrow_asset: ReserveToken, nonce=None,
                          interest_rate_mode: str = "stable") -> AaveTrade:
        """Same parameters as the self.borrow() function, except instead of 'borrow_amount', you will pass the
        percentage of borrowing power that you would like to borrow from in the 'borrow_percentage' parameter in the
        following format: 0.0 (0% of borrowing power) to 1.0 (100% of borrowing power)"""

        if borrow_percentage > 1.0:
            raise ValueError("Cannot borrow more than 100% of borrowing power. Please pass a value between 0.0 and 1.0")

        # Calculate borrow amount from available borrow percentage:
        total_borrowable_in_eth = self.get_user_data()[0]
        weth_to_borrow_asset = self.get_asset_price(base_address=self.get_reserve_token("WETH").address,
                                                    quote_address=borrow_asset.address)
        borrow_amount = weth_to_borrow_asset * (total_borrowable_in_eth * borrow_percentage)
        print(f"Borrowing {borrow_percentage * 100}% of total borrowing power: "
              f"{borrow_amount:.{borrow_asset.decimals}f} {borrow_asset.symbol}")

        return self.borrow(borrow_amount=borrow_amount, borrow_asset=borrow_asset, nonce=nonce,
                           interest_rate_mode=interest_rate_mode)

    def repay(self, repay_asset: ReserveToken, repay_amount: float, nonce=None,
              interest_rate_mode: str = "stable") -> AaveTrade:
        """
        Parameters:
            repay_asset: The ReserveToken object for the target asset to repay. Use self.get_reserve_token("SYMBOL") to
                         get the ReserveToken object.
            repay_amount: The amount of the target asset to repay. (e.g. 0.5 DAI)
            nonce: Manually specify the transaction count/ID. Leave as None to get the current transaction count from
                   the user's wallet set at self.wallet_address.
            interest_rate_mode: the type of borrow debt,'stable' or 'variable'

        Returns:
            The AaveTrade object - ./models.py

        https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#repay
        """
        print("Time to repay...")
        nonce = nonce if nonce else self.w3.eth.getTransactionCount(self.wallet_address)

        rate_mode_str = interest_rate_mode
        if interest_rate_mode == "stable":
            interest_rate_mode = 1
        else:
            interest_rate_mode = 2

        amount_in_decimal_units = self.convert_to_decimal_units(repay_asset, repay_amount)

        # First, attempt to approve the transaction:
        print(f"Approving transaction to repay {repay_amount} of {repay_asset.symbol} to Aave...")
        try:
            approval_hash, approval_gas = self.approve_erc20(erc20_address=repay_asset.address,
                                                             amount_in_decimal_units=amount_in_decimal_units,
                                                             nonce=nonce)
            print("Transaction approved!")
        except Exception as exc:
            raise UserWarning(f"Could not approve repay transaction - Error Code {exc}")

        print("Building function call...")
        function_call = self.lending_pool_contract.functions.repay(
            repay_asset.address,
            amount_in_decimal_units,
            interest_rate_mode,  # the the interest rate mode
            self.wallet_address,
        )
        print("Building transaction from function call...")
        transaction = function_call.buildTransaction(
            {
                "chainId": self.active_network.chain_id,
                "from": self.wallet_address,
                "nonce": nonce + 1 if approval_hash else nonce,
            }
        )
        print("Repaying...")
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.process_transaction_receipt(tx_hash, repay_amount, repay_asset, "Repay",
                                                   interest_rate_mode=rate_mode_str, approval_gas_cost=approval_gas)
        print(f"Repaid {repay_amount} {repay_asset.symbol}  |  "
              f"{self.get_user_data()[1]:.18f} ETH worth of debt remaining.")
        return receipt

    def repay_percentage(self, repay_asset: ReserveToken, repay_percentage: float, nonce=None) -> AaveTrade:
        """
        Same parameters as the self.repay() function, except instead of 'repay_amount', you will pass the
        percentage of outstanding debt that you would like to repay from in the 'repay_percentage' parameter using the
        following format:

        0.0 (0% of borrowing power) to 1.0 (100% of borrowing power)
        """

        if repay_percentage > 1.0:
            raise ValueError("Cannot repay more than 100% of debts. Please pass a value between 0.0 and 1.0")

        # Calculate debt amount from outstanding debt percentage:
        total_debt_in_eth = self.get_user_data()[1]
        weth_to_repay_asset = self.get_asset_price(base_address=self.get_reserve_token("WETH").address,
                                                   quote_address=repay_asset.address)
        repay_amount = weth_to_repay_asset * (total_debt_in_eth * repay_percentage)

        return self.repay(repay_asset, repay_amount, nonce)

    def get_abi(self, smart_contract_address: str):
        """
        Used to fetch the JSON ABIs for the deployed Aave smart contracts here:
        https://docs.aave.com/developers/v/2.0/deployed-contracts/deployed-contracts
        """
        print(f"Fetching ABI for smart contract: {smart_contract_address}")
        abi_endpoint = f'https://api.etherscan.io/api?module=contract&action=getabi&address={smart_contract_address}'

        retry_count = 0
        json_abi = None
        err = None
        while retry_count < 5:
            etherscan_response = requests.get(abi_endpoint).json()
            if str(etherscan_response['status']) == '0':
                err = etherscan_response['result']
                retry_count += 1
                time.sleep(1)
            else:
                try:
                    json_abi = json.loads(etherscan_response['result'])
                except json.decoder.JSONDecodeError:
                    err = "Could not load ABI into JSON format"
                except Exception as exc:
                    err = f"Response status was valid, but an unexpected error occurred '{exc}'"
                finally:
                    break
        if json_abi is not None:
            return json_abi
        else:
            raise Exception(f"Could not fetch ABI for contract: {smart_contract_address} - Error: {err}")

    def get_reserve_token(self, symbol: str) -> ReserveToken:
        """Returns the ReserveToken class containing the Aave reserve token with the passed symbol"""
        try:
            return [token for token in self.active_network.aave_tokens if token.symbol.lower() == symbol.lower()][0]
        except IndexError:
            raise ValueError(
                f"Could not match '{symbol}' with a valid reserve token on aave for the {self.active_network.net_name} network.")

    def fetch_reserve_tokens(self) -> list:
        """Returns all Aave ReserveToken class objects stored on the active network"""
        return self.active_network.aave_tokens

    def _get_erc20_contract(self, token_address: str) -> web3.eth.Contract:
        return self.w3.eth.contract(address=Web3.toChecksumAddress(token_address), abi=ABIReference.erc20_abi)

    def _initial_get_reserve_token(self, r_symbol: str, r_address: str) -> ReserveToken:
        """
        Builds the ReserveToken object by fetching data from the data provider contracts.
        Should only be used when initializing the active network's reserve token database. Otherwise, use get_reserve_token()

        :param r_symbol: The symbol of the reserve token's underlying asset (e.g. USDC)
        :param r_address: The reserve token address
        """
        r_erc = self._get_erc20_contract(r_address)
        r_decimals = r_erc.functions.decimals().call()
        print(f"Fetching Reserve Token: {r_symbol} ({r_decimals}) - {r_address}")

        # Build empty data structure to receive token mappings
        associated_tokens = {'aToken': {},
                             'stableDebtToken': {},
                             'variableDebtToken': {}}
        for key, token_address in zip(associated_tokens.keys(),
                                      self.data_provider_contract.functions.getReserveTokensAddresses(
                                          Web3.toChecksumAddress(r_address)).call()):
            # Get ERC20 contract to get token symbol
            erc = self._get_erc20_contract(token_address)
            token_symbol = erc.functions.symbol().call()
            associated_tokens[key] = {'address': token_address, 'symbol': token_symbol}

        return ReserveToken(r_symbol, r_address, r_decimals,
                            aTokenAddress=associated_tokens['aToken']['address'],
                            aTokenSymbol=associated_tokens['aToken']['symbol'],
                            stableDebtTokenAddress=associated_tokens['stableDebtToken']['address'],
                            stableDebtTokenSymbol=associated_tokens['stableDebtToken']['symbol'],
                            variableDebtTokenAddress=associated_tokens['variableDebtToken']['address'],
                            variableDebtTokenSymbol=associated_tokens['variableDebtToken']['symbol'])

    def _store_reserve_tokens(self) -> None:
        """
        Only run once when the client is initialized.
        Fetches and stores all reserve tokens and addresses for the set network.
        Concurrency using a process pool and futures.
        """
        reserves_tokens = self.data_provider_contract.functions.getAllReservesTokens().call()

        print("Building reserve tokens mapping... Please wait - this may take up to 60 seconds")
        # Run each multithread fetch to get realized token volatilities
        start = time.time()
        # output = []
        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     futures = [executor.submit(self._initial_get_reserve_token, symbol, address) for symbol, address in reserves_tokens]
        # for f in concurrent.futures.as_completed(futures):
        #     try:
        #         # self.active_network.aave_tokens.append(f.result())
        #         output.append(f.result())
        #     except Exception as exc:
        #         print("Could not store reserve token:", str(exc))
        for symbol, address in reserves_tokens:
            self.active_network.aave_tokens.append(self._initial_get_reserve_token(symbol, address))

        print(f"{len(self.active_network.aave_tokens)}/{len(reserves_tokens)} Reserve tokens stored for "
              f"{self.active_network.net_name} network in {(time.time() - start):.1f} seconds")

    def get_all_reserve_balances(self, hide_empty_assets: bool = True):
        """
        Get the current balance of each token type for each reserve token on Aave.
            - Supplied collateral amount
            - Stable debt amount
            - Variable debt amount
            - Current wallet balance of underlying asset

        :return: dict
            { # For each reserve token symbol:
            reserve_token_symbol: {
                collateral: supplied_collateral_amt
                stable_debt: stable_debt_amt,
                variable_debt: variable_debt_amt,
                wallet_balance: current_wallet_balance
                }
            }
        """

        # all_reserve_tokens = self.get_all_reserves_tokens()
        all_reserve_tokens = self.active_network.aave_tokens

        output = {token.symbol: {"collateral": 0, "stable_debt": 0, "variable_debt": 0, "wallet_balance": 0} for token in all_reserve_tokens}
        # Check each reserve token for debts
        for token in all_reserve_tokens:
            a_token_balance, stable_debt, variable_debt, _, _, _, _, _, _ = self.get_user_reserve_data(token)

            output[token.symbol]['collateral'] = a_token_balance
            output[token.symbol]["stable_debt"] = stable_debt
            output[token.symbol]["variable_debt"] = variable_debt

            erc20_contract = token.get_erc20_contract(self.w3)
            user_bal = erc20_contract.functions.balanceOf(self.wallet_address).call()
            output[token.symbol]["wallet_balance"] = user_bal

        if hide_empty_assets:
            for token, balances in output.copy().items():
                if all(v == 0 for v in [balances[k] for k in output[list(output.keys())[0]].keys()]):
                    output.pop(token)

        return output
