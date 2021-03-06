"""
PACKAGE REQUIREMENTS INSTALL COMMAND:

pip install --upgrade web3 requests
"""

from pprint import pprint
import json
import os
import time
from datetime import datetime
import requests
import web3.eth
from web3 import Web3
from web3.gas_strategies.time_based import *
from dataclasses import dataclass


"""------------------------------ Dataclass to Reference Aave Reserve Token Attributes ------------------------------"""
@dataclass
class ReserveToken:
    """Dataclass for easily accessing Aave reserve token properties"""
    aTokenAddress: str
    aTokenSymbol: str
    stableDebtTokenAddress: str
    variableDebtTokenAddress: str
    symbol: str
    address: str
    decimals: int


"""--------------------------- Dataclass to Neatly Handle Transaction Receipts ----------------------------"""
@dataclass
class AaveTrade:
    """Dataclass for easily accessing transaction receipt properties"""
    hash: str
    timestamp: int  # Unix timestamp
    datetime: str  # Formatted UTC datetime string: 'YYYY-MM-DD HH:MM:SS'
    contract_address: str
    from_address: str
    to_address: str
    gas_price: float  # The full amount in ETH paid for gas
    asset_symbol: str
    asset_address: str
    asset_amount: float  # In the token amount (not decimal units)
    asset_amount_decimal_units: int  # In decimal units (amount * 10^asset decimals)
    interest_rate_mode: str  # "stable", "variable", or None
    operation: str  # The operation description (e.g. deposit, borrow)


"""------------------------------------------ MAIN AAVE STAKING CLIENT ----------------------------------------------"""
class AaveStakingClient:
    """Fully plug-and-play AAVE staking client in Python3"""
    def __init__(self, WALLET_ADDRESS: str, PRIVATE_WALLET_KEY: str,
                 MAINNET_RPC_URL: str = None, KOVAN_RPC_URL: str = None,
                 GAS_STRATEGY: str = "medium"):

        self.private_key = PRIVATE_WALLET_KEY
        self.wallet_address = Web3.toChecksumAddress(WALLET_ADDRESS)

        if KOVAN_RPC_URL is None and MAINNET_RPC_URL is None:
            raise Exception("Missing RPC URLs for all available choices. Must use at least one network configuration.")
        elif KOVAN_RPC_URL is not None and MAINNET_RPC_URL is not None:
            raise Exception("Only one active network supported at a time. Please use either the Kovan or Mainnet network.")
        else:
            self.active_network = KovanConfig(KOVAN_RPC_URL) if KOVAN_RPC_URL is not None else MainnetConfig(
                MAINNET_RPC_URL)

        self.w3 = self._connect()

        if GAS_STRATEGY.lower() == "fast":
            """Transaction mined within 60 seconds."""
            self.w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
            self.timeout = 60
        elif GAS_STRATEGY.lower() == "medium":
            """Transaction mined within 5 minutes."""
            self.w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
            self.timeout = 60 * 5
        elif GAS_STRATEGY.lower() == "slow":
            """Transaction mined within 1 hour."""
            self.w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
            self.timeout = 60 * 60
        elif GAS_STRATEGY.lower() == "glacial":
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

    def get_lending_pool(self) -> web3.eth.Contract:
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

    def approve_erc20(self, erc20_address: str, lending_pool_contract: web3.eth.Contract, amount_in_decimal_units: int,
                      nonce=None) -> tuple:
        """
        Approve the smart contract to take the tokens out of the wallet
        For lending pool transactions, the 'lending_pool_contract' is the lending pool contract's address.

        Returns a tuple of the following:
            (transaction hash string, approval gas cost)
        """
        nonce = nonce if nonce else self.w3.eth.getTransactionCount(self.wallet_address)

        lending_pool_address = Web3.toChecksumAddress(lending_pool_contract.address)
        erc20_address = Web3.toChecksumAddress(erc20_address)
        erc20 = self.w3.eth.contract(address=erc20_address, abi=ABIReference.erc20_abi)
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

    def withdraw(self, withdraw_token: ReserveToken, withdraw_amount: float, lending_pool_contract: web3.eth.Contract,
                 nonce=None) -> AaveTrade:
        """
        Withdraws the amount of the withdraw_token from Aave, and burns the corresponding aToken.

        Parameters:
            withdraw_token: The ReserveToken object of the token to be withdrawn from Aave.

            withdraw_amount:  The amount of the 'withdraw_token' to withdraw from Aave (e.g. 0.001 WETH)

            lending_pool_contract: The lending pool contract object, obstantiated using self.get_lending_pool()

            nonce: Manually specify the transaction count/ID. Leave as None to get the current transaction count from
                   the user's wallet set at self.wallet_address.

        Returns:
            The AaveTrade object - See line 52 for datapoints reference

        Smart Contract Reference:
            https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#withdraw
        """
        nonce = nonce if nonce else self.w3.eth.getTransactionCount(self.wallet_address)
        amount_in_decimal_units = self.convert_to_decimal_units(withdraw_token, withdraw_amount)

        # First, attempt to approve the transaction:
        print(f"Approving transaction to withdraw {withdraw_amount:.{withdraw_token.decimals}f} of {withdraw_token.symbol} from Aave...")
        try:
            approval_hash, approval_gas = self.approve_erc20(erc20_address=withdraw_token.address,
                                                             lending_pool_contract=lending_pool_contract,
                                                             amount_in_decimal_units=amount_in_decimal_units,
                                                             nonce=nonce)
        except Exception as exc:
            raise UserWarning(f"Could not approve withdraw transaction - Error Code {exc}")

        # Second, if the transaction is approved, create the transaction to deposit the tokens to Aave:
        print(f"Withdrawing {withdraw_amount} of {withdraw_token.symbol} from Aave...")
        function_call = lending_pool_contract.functions.withdraw(withdraw_token.address,
                                                                 amount_in_decimal_units,
                                                                 self.wallet_address)
        transaction = function_call.buildTransaction(
            {
                "chainId": self.active_network.chain_id,
                "from": self.wallet_address,
                "nonce": nonce + 1,
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

    def withdraw_percentage(self, withdraw_token: ReserveToken, withdraw_percentage: float,
                            lending_pool_contract: web3.eth.Contract, nonce=None) -> AaveTrade:
        """Same parameters as the self.withdraw() function, except instead of 'withdraw_amount', you will pass the
        percentage of total available collateral on Aave that you would like to withdraw from in the 'withdraw_percentage'
        parameter in the following format: 0.0 (0% of borrowing power) to 1.0 (100% of borrowing power)"""

        if withdraw_percentage > 1.0:
            raise ValueError("Cannot withdraw more than 100% of available collateral of Aave. "
                             "Please pass a value between 0.0 and 1.0")

        # Calculate withdraw amount by multiplying the total collateral on Aave by the withdraw_percentage parameter.
        total_collateral = self.get_user_data(lending_pool_contract)[2]
        weth_to_withdraw_asset = self.get_asset_price(base_address=self.get_reserve_token("WETH").address,
                                                      quote_address=withdraw_token.address)
        withdraw_amount = weth_to_withdraw_asset * (total_collateral * withdraw_percentage)

        return self.withdraw(withdraw_token, withdraw_amount, lending_pool_contract, nonce)

    def deposit(self, deposit_token: ReserveToken, deposit_amount: float,
                lending_pool_contract: web3.eth.Contract, nonce=None) -> AaveTrade:
        """
        Deposits the 'deposit_amount' of the 'deposit_token' to Aave collateral.

        Parameters:
            deposit_token: The ReserveToken object of the token to be deposited/collateralized on Aave

            deposit_amount: The amount of the 'deposit_token' to deposit on Aave (e.g. 0.001 WETH)

            lending_pool_contract: The lending pool contract object, obstantiated using self.get_lending_pool()

            nonce: Manually specify the transaction count/ID. Leave as None to get the current transaction count from
                   the user's wallet set at self.wallet_address.

        Returns:
            The AaveTrade object - See line 52 for datapoints reference

        Smart Contract Reference:
            https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#deposit
        """

        nonce = nonce if nonce else self.w3.eth.getTransactionCount(self.wallet_address)

        amount_in_decimal_units = self.convert_to_decimal_units(deposit_token, deposit_amount)

        # First, attempt to approve the transaction:
        print(f"Approving transaction to deposit {deposit_amount} of {deposit_token.symbol} to Aave...")
        try:
            approval_hash, approval_gas = self.approve_erc20(erc20_address=deposit_token.address,
                                                             lending_pool_contract=lending_pool_contract,
                                                             amount_in_decimal_units=amount_in_decimal_units,
                                                             nonce=nonce)
        except Exception as exc:
            raise UserWarning(f"Could not approve deposit transaction - Error Code {exc}")

        # Second, if the transaction is approved, create the transaction to deposit the tokens to Aave:
        print(f"Depositing {deposit_amount} of {deposit_token.symbol} to Aave...")
        function_call = lending_pool_contract.functions.deposit(deposit_token.address,
                                                                amount_in_decimal_units,
                                                                self.wallet_address,
                                                                0)  # The 0 is deprecated and must persist
        transaction = function_call.buildTransaction(
            {
                "chainId": self.active_network.chain_id,
                "from": self.wallet_address,
                "nonce": nonce + 1,
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

    def get_user_data(self, lending_pool_contract: web3.eth.Contract) -> tuple:
        """
        - Fetches user account data (shown below) across all reserves
        - Only returns the borrowing power (in ETH), and the total user debt (in ETH)

        Parameters:
            lending_pool_contract: The web3.eth.Contract object fetched from self.get_lending_pool() to represent the
            Aave lending pool smart contract.

        https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#getuseraccountdata
        """
        user_data = lending_pool_contract.functions.getUserAccountData(self.wallet_address).call()
        try:
            (
                total_collateral_eth,  # total collateral in ETH of the use (wei decimal unit)
                total_debt_eth,  # total debt in ETH of the user (wei decimal unit)
                available_borrow_eth,  # borrowing power left of the user (wei decimal unit)
                current_liquidation_threshold,
                # liquidation threshold of the user (1e4 format => percentage plus two decimals)
                tlv,  # Loan To Value of the user (1e4 format => percentage plus two decimals)
                health_factor,  # current health factor of the user
            ) = user_data
        except TypeError:
            raise Exception(f"Could not unpack user data due to a TypeError - Received: {user_data}")

        available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
        total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
        total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
        # print(f"Total Collateral Assets: {total_collateral_eth:.18f} ETH")
        # print(f"Total Borrowed Assets: {total_debt_eth:.18f} ETH")
        # print(f"Total Borrowing Power: {available_borrow_eth:.18f} ETH")
        return float(available_borrow_eth), float(total_debt_eth), float(total_collateral_eth)

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

    def borrow(self, lending_pool_contract: web3.eth.Contract, borrow_amount: float, borrow_asset: ReserveToken,
               nonce=None, interest_rate_mode: str = "stable") -> AaveTrade:
        """
        Borrows the underlying asset (erc20_address) as long as the amount is within the confines of
        the user's buying power.

        Parameters:
            lending_pool_contract: The web3.eth.Contract class object fetched from the self.get_lending_pool function.
            borrow_amount: Amount of the underlying asset to borrow. The amount should be measured in the asset's
                           currency (e.g. for ETH, borrow_amount=0.05, as in 0.05 ETH)
            borrow_asset: The ReserveToken which you want to borrow from Aave. To get the reserve token, you can use the
                          self.get_reserve_token(symbol: str) function.
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
        function_call = lending_pool_contract.functions.borrow(Web3.toChecksumAddress(borrow_asset.address),
                                                               borrow_amount_in_decimal_units,
                                                               interest_rate_mode, 0,
                                                               # 0 must not be changed, it is deprecated
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
        print(f"Remaining Borrowing Power: {self.get_user_data(lending_pool_contract)[0]:.18f}")
        print(f"Transaction Hash: {tx_hash.hex()}")
        return receipt

    def convert_to_decimal_units(self, reserve_token: ReserveToken, token_amount: float) -> int:
        """integer units i.e amt * 10 ^ (decimal units of the token). So, 1.2 USDC will be 1.2 * 10 ^ 6"""
        return int(token_amount * (10 ** int(reserve_token.decimals)))

    def borrow_percentage(self, lending_pool_contract: web3.eth.Contract, borrow_percentage: float,
                          borrow_asset: ReserveToken, nonce=None, interest_rate_mode: str = "stable") -> AaveTrade:
        """Same parameters as the self.borrow() function, except instead of 'borrow_amount', you will pass the
        percentage of borrowing power that you would like to borrow from in the 'borrow_percentage' parameter in the
        following format: 0.0 (0% of borrowing power) to 1.0 (100% of borrowing power)"""

        if borrow_percentage > 1.0:
            raise ValueError("Cannot borrow more than 100% of borrowing power. Please pass a value between 0.0 and 1.0")

        # Calculate borrow amount from available borrow percentage:
        total_borrowable_in_eth = self.get_user_data(lending_pool_contract)[0]
        weth_to_borrow_asset = self.get_asset_price(base_address=self.get_reserve_token("WETH").address,
                                                    quote_address=borrow_asset.address)
        borrow_amount = weth_to_borrow_asset * (total_borrowable_in_eth * borrow_percentage)
        print(f"Borrowing {borrow_percentage * 100}% of total borrowing power: "
              f"{borrow_amount:.{borrow_asset.decimals}f} {borrow_asset.symbol}")

        return self.borrow(lending_pool_contract=lending_pool_contract, borrow_amount=borrow_amount,
                           borrow_asset=borrow_asset, nonce=nonce, interest_rate_mode=interest_rate_mode)

    def repay(self, lending_pool_contract: web3.eth.Contract, repay_amount: float, repay_asset: ReserveToken,
              nonce=None, interest_rate_mode: str = "stable") -> AaveTrade:
        """
        Parameters:
            lending_pool_contract: The web3.eth.Contract object returned by the self.get_lending_pool() function.
            repay_amount: The amount of the target asset to repay. (e.g. 0.5 DAI)
            repay_asset: The ReserveToken object for the target asset to repay. Use self.get_reserve_token("SYMBOL") to
                         get the ReserveToken object.
            nonce: Manually specify the transaction count/ID. Leave as None to get the current transaction count from
                   the user's wallet set at self.wallet_address.
            interest_rate_mode: the type of borrow debt,'stable' or 'variable'

        Returns:
            The AaveTrade object - See line 52 for datapoints reference

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
                                                             lending_pool_contract=lending_pool_contract,
                                                             amount_in_decimal_units=amount_in_decimal_units,
                                                             nonce=nonce)
            print("Transaction approved!")
        except Exception as exc:
            raise UserWarning(f"Could not approve repay transaction - Error Code {exc}")

        print("Building function call...")
        function_call = lending_pool_contract.functions.repay(
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
                "nonce": nonce + 1,
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
              f"{self.get_user_data(lending_pool_contract)[1]:.18f} ETH worth of debt remaining.")
        return receipt

    def repay_percentage(self, lending_pool_contract: web3.eth.Contract, repay_percentage: float,
                         repay_asset: ReserveToken, nonce=None) -> AaveTrade:
        """
        Same parameters as the self.repay() function, except instead of 'repay_amount', you will pass the
        percentage of outstanding debt that you would like to repay from in the 'repay_percentage' parameter using the
        following format:

        0.0 (0% of borrowing power) to 1.0 (100% of borrowing power)
        """

        if repay_percentage > 1.0:
            raise ValueError("Cannot repay more than 100% of debts. Please pass a value between 0.0 and 1.0")

        # Calculate debt amount from outstanding debt percentage:
        total_debt_in_eth = self.get_user_data(lending_pool_contract)[1]
        weth_to_repay_asset = self.get_asset_price(base_address=self.get_reserve_token("WETH").address,
                                                   quote_address=repay_asset.address)
        repay_amount = weth_to_repay_asset * (total_debt_in_eth * repay_percentage)

        return self.repay(lending_pool_contract, repay_amount, repay_asset, nonce)

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
            raise Exception(f"could not fetch ABI for contract: {smart_contract_address} - Error: {err}")

    def get_reserve_token(self, symbol: str) -> ReserveToken:
        """Returns the ReserveToken class containing the Aave reserve token with the passed symbol"""
        try:
            return [token for token in self.active_network.aave_tokens
                    if token.symbol.lower() == symbol.lower() or token.aTokenSymbol.lower() == symbol.lower()][0]
        except IndexError:
            raise ValueError(
                f"Could not match '{symbol}' with a valid reserve token on aave for the {self.active_network.net_name} network.")

    def list_reserve_tokens(self) -> list:
        """Returns all Aave ReserveToken class objects stored on the active network"""
        return self.active_network.aave_tokens


"""----------------------------------- NETWORK CONFIG & ABI REFERENCE DATACLASSES ----------------------------------"""
class KovanConfig:
    def __init__(self, kovan_rpc_url: str):
        self.net_name = "Kovan"
        self.chain_id = 42
        self.lending_pool_addresses_provider = '0x88757f2f99175387aB4C6a4b3067c77A695b0349'
        self.weth_token = '0xd0a1e359811322d97991e03f863a0c30c2cf029c'
        # https://aave.github.io/aave-addresses/kovan.json
        # Aave uses their own testnet tokens to ensure they are good
        # find the most up to date in the above
        self.rpc_url = kovan_rpc_url
        self.aave_tokenlist_url = "https://aave.github.io/aave-addresses/kovan.json"
        self.aave_tokens = [ReserveToken(**token_data) for token_data in self.fetch_aave_tokens()]

    def fetch_aave_tokens(self) -> dict:
        try:
            return requests.get(self.aave_tokenlist_url).json()['proto']
        except:
            raise ConnectionError("Could not fetch Aave tokenlist for the Kovan network from URL: "
                                  "https://aave.github.io/aave-addresses/kovan.json")


class MainnetConfig:
    def __init__(self, mainnet_rpc_url: str):
        self.net_name = "Mainnet"
        self.chain_id = 1337
        self.lending_pool_addresses_provider = '0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5'
        self.weth_token = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
        # For mainnet, the link token is the same as the aave token
        self.link_token = '0x514910771af9ca656af840dff83e8264ecf986ca'
        # self.aave_link_token = '0x514910771af9ca656af840dff83e8264ecf986ca'
        self.rpc_url = mainnet_rpc_url
        self.aave_tokenlist_url = "https://aave.github.io/aave-addresses/mainnet.json"
        self.aave_tokens = [ReserveToken(**token_data) for token_data in self.fetch_aave_tokens()]

    def fetch_aave_tokens(self) -> dict:
        try:
            return requests.get(self.aave_tokenlist_url).json()['proto']
        except:
            raise ConnectionError("Could not fetch Aave tokenlist for the Mainnet network from URL: "
                                  "https://aave.github.io/aave-addresses/mainnet.json")


class ABIReference:
    """
    This class contains full JSON ABIs for the smart contracts being called in this client.

    Eventually, I will implement a method to call these ABIs from the etherscan API when they are needed, instead of
    utilizing this class structure which results in hundreds of redundant lines.

    Disregard all past this line, unless you need to add an ABI to implement more smart contracts.
    """
    weth_abi = [
        {
            "constant": True,
            "inputs": [],
            "name": "name",
            "outputs": [{"name": "tokenName", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"},
            ],
            "name": "approve",
            "outputs": [{"name": "success", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "totalTokensIssued", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
            ],
            "name": "transferFrom",
            "outputs": [{"name": "success", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "decimalPlaces", "type": "uint8"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [{"name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "tokenSymbol", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
            ],
            "name": "transfer",
            "outputs": [{"name": "success", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [],
            "name": "deposit",
            "outputs": [],
            "payable": True,
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [
                {"name": "owner", "type": "address"},
                {"name": "spender", "type": "address"},
            ],
            "name": "allowance",
            "outputs": [{"name": "remaining", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
    ]

    price_feed_abi = [
        {
            "inputs": [],
            "name": "decimals",
            "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "description",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint80", "name": "_roundId", "type": "uint80"}],
            "name": "getRoundData",
            "outputs": [
                {"internalType": "uint80", "name": "roundId", "type": "uint80"},
                {"internalType": "int256", "name": "answer", "type": "int256"},
                {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
                {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
                {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "latestRoundData",
            "outputs": [
                {"internalType": "uint80", "name": "roundId", "type": "uint80"},
                {"internalType": "int256", "name": "answer", "type": "int256"},
                {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
                {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
                {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "version",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    erc20_abi = [
        {
            "inputs": [
                {"internalType": "address", "name": "owner", "type": "address"},
                {"internalType": "address", "name": "spender", "type": "address"},
            ],
            "name": "allowance",
            "outputs": [
                {"internalType": "uint256", "name": "remaining", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "spender", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
            ],
            "name": "approve",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"internalType": "uint256", "name": "balance", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "decimals",
            "outputs": [
                {"internalType": "uint8", "name": "decimalPlaces", "type": "uint8"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "spender", "type": "address"},
                {"internalType": "uint256", "name": "addedValue", "type": "uint256"},
            ],
            "name": "decreaseApproval",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "spender", "type": "address"},
                {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"},
            ],
            "name": "increaseApproval",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [{"internalType": "string", "name": "tokenName", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "symbol",
            "outputs": [
                {"internalType": "string", "name": "tokenSymbol", "type": "string"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "totalSupply",
            "outputs": [
                {"internalType": "uint256", "name": "totalTokensIssued", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
            ],
            "name": "transfer",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
                {"internalType": "bytes", "name": "data", "type": "bytes"},
            ],
            "name": "transferAndCall",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "from", "type": "address"},
                {"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
            ],
            "name": "transferFrom",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]

    lending_pool_addresses_provider_abi = [
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "id",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "hasProxy",
                    "type": "bool",
                },
            ],
            "name": "AddressSet",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "ConfigurationAdminUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "EmergencyAdminUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "LendingPoolCollateralManagerUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "LendingPoolConfiguratorUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "LendingPoolUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "LendingRateOracleUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "string",
                    "name": "newMarketId",
                    "type": "string",
                }
            ],
            "name": "MarketIdSet",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "PriceOracleUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "id",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                },
            ],
            "name": "ProxyCreated",
            "type": "event",
        },
        {
            "inputs": [{"internalType": "bytes32", "name": "id", "type": "bytes32"}],
            "name": "getAddress",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getEmergencyAdmin",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getLendingPool",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getLendingPoolCollateralManager",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getLendingPoolConfigurator",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getLendingRateOracle",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getMarketId",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getPoolAdmin",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getPriceOracle",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                {"internalType": "address", "name": "newAddress", "type": "address"},
            ],
            "name": "setAddress",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                {"internalType": "address", "name": "impl", "type": "address"},
            ],
            "name": "setAddressAsProxy",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "admin", "type": "address"}],
            "name": "setEmergencyAdmin",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "manager", "type": "address"}],
            "name": "setLendingPoolCollateralManager",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "configurator", "type": "address"}
            ],
            "name": "setLendingPoolConfiguratorImpl",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "pool", "type": "address"}],
            "name": "setLendingPoolImpl",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "lendingRateOracle", "type": "address"}
            ],
            "name": "setLendingRateOracle",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "string", "name": "marketId", "type": "string"}],
            "name": "setMarketId",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "admin", "type": "address"}],
            "name": "setPoolAdmin",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "priceOracle", "type": "address"}
            ],
            "name": "setPriceOracle",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]

    lending_pool_abi = [
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "onBehalfOf",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "borrowRateMode",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "borrowRate",
                    "type": "uint256",
                },
                {
                    "indexed": True,
                    "internalType": "uint16",
                    "name": "referral",
                    "type": "uint16",
                },
            ],
            "name": "Borrow",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "onBehalfOf",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
                {
                    "indexed": True,
                    "internalType": "uint16",
                    "name": "referral",
                    "type": "uint16",
                },
            ],
            "name": "Deposit",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "target",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "initiator",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "asset",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "premium",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint16",
                    "name": "referralCode",
                    "type": "uint16",
                },
            ],
            "name": "FlashLoan",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "collateralAsset",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "debtAsset",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "debtToCover",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "liquidatedCollateralAmount",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "liquidator",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "receiveAToken",
                    "type": "bool",
                },
            ],
            "name": "LiquidationCall",
            "type": "event",
        },
        {"anonymous": False, "inputs": [], "name": "Paused", "type": "event"},
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
            ],
            "name": "RebalanceStableBorrowRate",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "repayer",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Repay",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "liquidityRate",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "stableBorrowRate",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "variableBorrowRate",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "liquidityIndex",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "variableBorrowIndex",
                    "type": "uint256",
                },
            ],
            "name": "ReserveDataUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
            ],
            "name": "ReserveUsedAsCollateralDisabled",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
            ],
            "name": "ReserveUsedAsCollateralEnabled",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "rateMode",
                    "type": "uint256",
                },
            ],
            "name": "Swap",
            "type": "event",
        },
        {"anonymous": False, "inputs": [], "name": "Unpaused", "type": "event"},
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Withdraw",
            "type": "event",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "uint256", "name": "interestRateMode", "type": "uint256"},
                {"internalType": "uint16", "name": "referralCode", "type": "uint16"},
                {"internalType": "address", "name": "onBehalfOf", "type": "address"},
            ],
            "name": "borrow",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "address", "name": "onBehalfOf", "type": "address"},
                {"internalType": "uint16", "name": "referralCode", "type": "uint16"},
            ],
            "name": "deposit",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "address", "name": "from", "type": "address"},
                {"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "uint256", "name": "balanceFromAfter", "type": "uint256"},
                {"internalType": "uint256", "name": "balanceToBefore", "type": "uint256"},
            ],
            "name": "finalizeTransfer",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "receiverAddress", "type": "address"},
                {"internalType": "address[]", "name": "assets", "type": "address[]"},
                {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"},
                {"internalType": "uint256[]", "name": "modes", "type": "uint256[]"},
                {"internalType": "address", "name": "onBehalfOf", "type": "address"},
                {"internalType": "bytes", "name": "params", "type": "bytes"},
                {"internalType": "uint16", "name": "referralCode", "type": "uint16"},
            ],
            "name": "flashLoan",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getAddressesProvider",
            "outputs": [
                {
                    "internalType": "contract ILendingPoolAddressesProvider",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
            "name": "getConfiguration",
            "outputs": [
                {
                    "components": [
                        {"internalType": "uint256", "name": "data", "type": "uint256"}
                    ],
                    "internalType": "struct DataTypes.ReserveConfigurationMap",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
            "name": "getReserveData",
            "outputs": [
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "uint256",
                                    "name": "data",
                                    "type": "uint256",
                                }
                            ],
                            "internalType": "struct DataTypes.ReserveConfigurationMap",
                            "name": "configuration",
                            "type": "tuple",
                        },
                        {
                            "internalType": "uint128",
                            "name": "liquidityIndex",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint128",
                            "name": "variableBorrowIndex",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint128",
                            "name": "currentLiquidityRate",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint128",
                            "name": "currentVariableBorrowRate",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint128",
                            "name": "currentStableBorrowRate",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint40",
                            "name": "lastUpdateTimestamp",
                            "type": "uint40",
                        },
                        {
                            "internalType": "address",
                            "name": "aTokenAddress",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "stableDebtTokenAddress",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "variableDebtTokenAddress",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "interestRateStrategyAddress",
                            "type": "address",
                        },
                        {"internalType": "uint8", "name": "id", "type": "uint8"},
                    ],
                    "internalType": "struct DataTypes.ReserveData",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
            "name": "getReserveNormalizedIncome",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
            "name": "getReserveNormalizedVariableDebt",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getReservesList",
            "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
            "name": "getUserAccountData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "totalCollateralETH",
                    "type": "uint256",
                },
                {"internalType": "uint256", "name": "totalDebtETH", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "availableBorrowsETH",
                    "type": "uint256",
                },
                {
                    "internalType": "uint256",
                    "name": "currentLiquidationThreshold",
                    "type": "uint256",
                },
                {"internalType": "uint256", "name": "ltv", "type": "uint256"},
                {"internalType": "uint256", "name": "healthFactor", "type": "uint256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
            "name": "getUserConfiguration",
            "outputs": [
                {
                    "components": [
                        {"internalType": "uint256", "name": "data", "type": "uint256"}
                    ],
                    "internalType": "struct DataTypes.UserConfigurationMap",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "reserve", "type": "address"},
                {"internalType": "address", "name": "aTokenAddress", "type": "address"},
                {"internalType": "address", "name": "stableDebtAddress", "type": "address"},
                {
                    "internalType": "address",
                    "name": "variableDebtAddress",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "interestRateStrategyAddress",
                    "type": "address",
                },
            ],
            "name": "initReserve",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "collateralAsset", "type": "address"},
                {"internalType": "address", "name": "debtAsset", "type": "address"},
                {"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint256", "name": "debtToCover", "type": "uint256"},
                {"internalType": "bool", "name": "receiveAToken", "type": "bool"},
            ],
            "name": "liquidationCall",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "paused",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "address", "name": "user", "type": "address"},
            ],
            "name": "rebalanceStableBorrowRate",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "uint256", "name": "rateMode", "type": "uint256"},
                {"internalType": "address", "name": "onBehalfOf", "type": "address"},
            ],
            "name": "repay",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "reserve", "type": "address"},
                {"internalType": "uint256", "name": "configuration", "type": "uint256"},
            ],
            "name": "setConfiguration",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bool", "name": "val", "type": "bool"}],
            "name": "setPause",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "reserve", "type": "address"},
                {
                    "internalType": "address",
                    "name": "rateStrategyAddress",
                    "type": "address",
                },
            ],
            "name": "setReserveInterestRateStrategyAddress",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "bool", "name": "useAsCollateral", "type": "bool"},
            ],
            "name": "setUserUseReserveAsCollateral",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "rateMode", "type": "uint256"},
            ],
            "name": "swapBorrowRateMode",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "address", "name": "to", "type": "address"},
            ],
            "name": "withdraw",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]

    aave_price_oracle_abi = [
        {
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "_assets",
                    "type": "address[]"
                },
                {
                    "internalType": "address[]",
                    "name": "_sources",
                    "type": "address[]"
                },
                {
                    "internalType": "address",
                    "name": "_fallbackOracle",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "source",
                    "type": "address"
                }
            ],
            "name": "AssetSourceUpdated",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "fallbackOracle",
                    "type": "address"
                }
            ],
            "name": "FallbackOracleUpdated",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "previousOwner",
                    "type": "address"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address"
                }
            ],
            "name": "OwnershipTransferred",
            "type": "event"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "isOwner",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [],
            "name": "renounceOwnership",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address"
                }
            ],
            "name": "transferOwnership",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "_assets",
                    "type": "address[]"
                },
                {
                    "internalType": "address[]",
                    "name": "_sources",
                    "type": "address[]"
                }
            ],
            "name": "setAssetSources",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_fallbackOracle",
                    "type": "address"
                }
            ],
            "name": "setFallbackOracle",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_asset",
                    "type": "address"
                }
            ],
            "name": "getAssetPrice",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "_assets",
                    "type": "address[]"
                }
            ],
            "name": "getAssetsPrices",
            "outputs": [
                {
                    "internalType": "uint256[]",
                    "name": "",
                    "type": "uint256[]"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_asset",
                    "type": "address"
                }
            ],
            "name": "getSourceOfAsset",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "getFallbackOracle",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]

    protocol_data_provider_contract_address = "0x057835Ad21177dbdd3090bB1CAE03EaCF78Fc6d"
    protocol_data_provider = [
        {
            "inputs": [
                {
                    "internalType": "contract ILendingPoolAddressesProvider",
                    "name": "addressesProvider",
                    "type": "address"
                }
            ],
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "inputs": [],
            "name": "ADDRESSES_PROVIDER",
            "outputs": [
                {
                    "internalType": "contract ILendingPoolAddressesProvider",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getAllATokens",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "string",
                            "name": "symbol",
                            "type": "string"
                        },
                        {
                            "internalType": "address",
                            "name": "tokenAddress",
                            "type": "address"
                        }
                    ],
                    "internalType": "struct AaveProtocolDataProvider.TokenData[]",
                    "name": "",
                    "type": "tuple[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getAllReservesTokens",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "string",
                            "name": "symbol",
                            "type": "string"
                        },
                        {
                            "internalType": "address",
                            "name": "tokenAddress",
                            "type": "address"
                        }
                    ],
                    "internalType": "struct AaveProtocolDataProvider.TokenData[]",
                    "name": "",
                    "type": "tuple[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                }
            ],
            "name": "getReserveConfigurationData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "decimals",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "ltv",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidationThreshold",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidationBonus",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "reserveFactor",
                    "type": "uint256"
                },
                {
                    "internalType": "bool",
                    "name": "usageAsCollateralEnabled",
                    "type": "bool"
                },
                {
                    "internalType": "bool",
                    "name": "borrowingEnabled",
                    "type": "bool"
                },
                {
                    "internalType": "bool",
                    "name": "stableBorrowRateEnabled",
                    "type": "bool"
                },
                {
                    "internalType": "bool",
                    "name": "isActive",
                    "type": "bool"
                },
                {
                    "internalType": "bool",
                    "name": "isFrozen",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                }
            ],
            "name": "getReserveData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "availableLiquidity",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "totalStableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "totalVariableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidityRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "variableBorrowRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "stableBorrowRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "averageStableBorrowRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidityIndex",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "variableBorrowIndex",
                    "type": "uint256"
                },
                {
                    "internalType": "uint40",
                    "name": "lastUpdateTimestamp",
                    "type": "uint40"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                }
            ],
            "name": "getReserveTokensAddresses",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "aTokenAddress",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "stableDebtTokenAddress",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "variableDebtTokenAddress",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "user",
                    "type": "address"
                }
            ],
            "name": "getUserReserveData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "currentATokenBalance",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "currentStableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "currentVariableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "principalStableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "scaledVariableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "stableBorrowRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidityRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint40",
                    "name": "stableRateLastUpdated",
                    "type": "uint40"
                },
                {
                    "internalType": "bool",
                    "name": "usageAsCollateralEnabled",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]


