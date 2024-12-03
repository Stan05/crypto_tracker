# crypto_tracker/models.py

from datetime import datetime
from enum import Enum


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


class ChainIdType(BaseEnum):
    ETHEREUM = "ethereum"
    BASE = "base"
    SOLANA = "solana"


class DexIdType(BaseEnum):
    UNISWAP = "uniswap"
    KYBERSWAP = "kyberswap"
    MATCHA = "matcha"

class TransactionStatusType(BaseEnum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class TransactionResponseType(BaseEnum):
    GRT_UNISWAP_V3_BASE = "Base.Uniswap-V3.Subgraph"
    KYBERSWAP_BASE = "KyberSwap.Subgraph"