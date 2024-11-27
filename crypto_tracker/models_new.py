# crypto_tracker/models_new.py

from enum import Enum

class TradeType(Enum):
    BUY = "buy"
    SELL = "sell"

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name.upper()]  # Convert to uppercase for case-insensitive matching
        except KeyError:
            raise ValueError(f"{name} is not a valid {cls.__name__}")

class ChainIdType(Enum):
    ETHEREUM = "ethereum"
    BASE = "base"
    SOLANA = "solana"

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name.upper()]  # Convert to uppercase for case-insensitive matching
        except KeyError:
            raise ValueError(f"{name} is not a valid {cls.__name__}")