# crypto_tracker/models_new.py

from enum import Enum

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