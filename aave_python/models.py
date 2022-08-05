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