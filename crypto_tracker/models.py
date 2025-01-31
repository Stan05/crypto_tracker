# crypto_tracker/models.py

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


#### Domain

class Trade:
    def __init__(self, order_id, symbol, price, qty, side, status, platform, created_on, updated_on):
        self.order_id:int = order_id
        self.symbol:Symbol = symbol
        self.price:float = price
        self.qty:float = qty
        self.side:str = side
        self.status:str = status
        self.platform:str = platform
        self.created_on:datetime = created_on
        self.updated_on:datetime = updated_on
    
    def __repr__(self):
        return f"<Trade order_id={self.order_id}, symbol={self.symbol}, price={self.price}, qty={self.qty}, side={self.side}, status={self.status}, platform={self.platform}, created_on={self.created_on}, updated_on={self.updated_on}>"

class Symbol:
    def __init__(self, ticker_buy, ticker_sell):
        self.ticker_buy = ticker_buy
        self.ticker_sell = ticker_sell
    
    @classmethod
    def from_symbol_with_separator(self, symbol:str):
        """Alternative constructor that sets default values for other fields."""
        return self(symbol.split("/")[0], symbol.split("/")[1])
    
    def with_separator(self):
        return self.ticker_buy + "/" + self.ticker_sell

    def to_plain_text(self):
        return self.ticker_buy + self.ticker_sell
    
    def __repr__(self):
        return f"<Symbol {self.to_plain_text()}>"
    
    def __eq__(self, other):
        """Check if two Symbol objects are equal based on ticker_buy and ticker_sell."""
        if isinstance(other, Symbol):
            return self.ticker_buy == other.ticker_buy and self.ticker_sell == other.ticker_sell
        return False
    
    def __hash__(self):
        """Generate a hash value based on ticker_buy and ticker_sell."""
        return hash((self.ticker_buy, self.ticker_sell))


class BaseEnum(Enum):

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name.upper()]  # Convert to uppercase for case-insensitive matching
        except KeyError:
            raise ValueError(f"{name} is not a valid {cls.__name__}")


class TradeType(BaseEnum):
    BUY = "buy"
    SELL = "sell"

class TradeStatus(BaseEnum):
    IN_TRADE = "In Trade"
    SOLD = "Sold"
    MOON_BAG = "Moon Bag"

class ChainIdType(BaseEnum):
    ETHEREUM = "ethereum"
    BASE = "base"
    SOLANA = "solana"


class DexIdType(BaseEnum):
    UNISWAP = "uniswap"
    KYBERSWAP = "kyberswap"
    MATCHA = "matcha"
    VIRTUALS = "virtuals"

class TransactionStatusType(BaseEnum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class TransactionResponseType(BaseEnum):
    GRT_UNISWAP_V3_BASE = "Base.Uniswap-V3.Subgraph"
    KYBERSWAP_BASE = "KyberSwap.Subgraph"

class Token(BaseModel):
    address: str
    name: str
    symbol: str

class Swap(BaseModel):
    base_token_amount: float
    quote_token_amount: float
    amount_USD: float
    origin: str
    base_token: Token
    quote_token: Token
    timestamp: datetime
    pool_id: str
    trade_type: TradeType

class Transaction(BaseModel):
    id: str
    swap: Swap
    payload: dict

class AggregatedTrade:
    def __init__(self, pair_id, pair, total_buy_quantity, total_buy_native_value, total_buy_usd_value,
                 total_sell_quantity, total_sell_native_value, total_sell_usd_value):
        self.pair_id: int = pair_id
        self.pair: str = pair

        self.total_buy_quantity: float = total_buy_quantity
        self.total_buy_native_value: float = total_buy_native_value
        self.total_buy_usd_value: float = total_buy_usd_value

        self.total_sell_quantity: float = total_sell_quantity
        self.total_sell_native_value: float = total_sell_native_value
        self.total_sell_usd_value: float = total_sell_usd_value

    def __repr__(self):
        return (
            f"AggregatedTrade("
            f"pair_id={self.pair_id}, "
            f"pair='{self.pair}', "
            f"total_buy_quantity={self.total_buy_quantity}, "
            f"total_buy_native_value={self.total_buy_native_value}, "
            f"total_buy_usd_value={self.total_buy_usd_value}, "
            f"total_sell_quantity={self.total_sell_quantity}, "
            f"total_sell_native_value={self.total_sell_native_value}, "
            f"total_sell_usd_value={self.total_sell_usd_value})"
        )

