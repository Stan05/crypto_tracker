# crypto_tracker/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, BigInteger
from datetime import datetime
from sqlalchemy.orm import declarative_base

# ORMs

Base = declarative_base()

class TradeORM(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    order_id = Column(BigInteger, unique=True, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    qty = Column(Float, nullable=False)
    side = Column(String, nullable=False)
    status = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<TradeORM(id={self.id}, order_id={self.order_id}, symbol={self.symbol})>"
    
    @staticmethod
    def order_id_unique_constraint_name():
        return "trades_order_id_key"
    
class TradePairORM(Base):
    __tablename__ = 'trade_pairs'
    ## TODO: Rename created_on and updated_on to first_trade_created_on last_trade_updated_on
    id = Column(Integer, primary_key=True)
    ticker_buy = Column(String, nullable=False)
    ticker_sell = Column(String, nullable=False)
    average_buy_price = Column(Float, nullable=True)
    available_quantity = Column(Float, nullable=True) 
    first_trade_created_on = Column(DateTime, nullable=False)
    last_trade_updated_on = Column(DateTime, nullable=False)
    trades_updated_on = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint('ticker_buy', 'ticker_sell', name='uix_ticker_buy_ticker_sell'),)

    def map_to_model(self) -> 'TradePair':
       return TradePair(
           ticker_buy=self.ticker_buy,
           ticker_sell=self.ticker_sell,
           average_buy_price=self.average_buy_price,
           available_quantity=self.available_quantity,
           first_trade_created_on=self.first_trade_created_on,
           last_trade_updated_on=self.last_trade_updated_on,
           trades_updated_on=self.trades_updated_on
           )
    
    def __repr__(self):
        return f"<TradePairORM(ticker_buy={self.ticker_buy}, ticker_sell={self.ticker_sell})>"
    
    @staticmethod
    def ticker_unique_constrant_name():
        return "uix_ticker_buy_ticker_sell"
    
class PairPriceSnapshotORM(Base):
    __tablename__ = 'pair_price_snapshot'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    current_price = Column(Float, nullable=False) 
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)

    def map_to_model(self) -> 'PairPriceSnapshot':
       return PairPriceSnapshot(
           symbol=Symbol.from_symbol_with_separator(self.symbol),
           current_price=self.current_price,
           created_on=self.created_on,
           updated_on=self.updated_on
           )
    
    def __repr__(self):
        return f"<PairPriceSnapshotORM(symbol={self.symbol}, current_price={self.current_price}), updated_on={self.updated_on}>"

    @staticmethod
    def symbol_unique_constrant_name():
        return "pair_price_snapshot_symbol_key"

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

    def map_to_orm(self) -> dict:
        """
        Maps the Trade object to a dictionary of ORM-compatible values for insertion.
        """
        return {
            TradeORM.order_id: self.order_id,
            TradeORM.symbol: self.symbol.with_separator(),
            TradeORM.price: self.price,
            TradeORM.qty: self.qty,
            TradeORM.side: self.side,
            TradeORM.status: self.status,
            TradeORM.platform: self.platform,
            TradeORM.created_on: self.created_on,  
            TradeORM.updated_on: self.updated_on   
        }
    
    def __repr__(self):
        return f"<Trade order_id={self.order_id}, symbol={self.symbol}, price={self.price}, qty={self.qty}, side={self.side}, status={self.status}, platform={self.platform}, created_on={self.created_on}, updated_on={self.updated_on}>"
    
class TradePair:
    def __init__(self, ticker_buy, ticker_sell, average_buy_price, available_quantity, first_trade_created_on, last_trade_updated_on, trades_updated_on):
        self.ticker_buy = ticker_buy
        self.ticker_sell = ticker_sell
        self.average_buy_price = average_buy_price
        self.available_quantity = available_quantity
        self.first_trade_created_on = first_trade_created_on
        self.last_trade_updated_on = last_trade_updated_on
        self.trades_updated_on = trades_updated_on
    
    def map_to_orm(self) -> dict:
        """
        Maps the TradePair object to a dictionary that can be used with SQLAlchemy's insert() or update() methods.
        """
        return {
            TradePairORM.ticker_buy: self.ticker_buy,
            TradePairORM.ticker_sell: self.ticker_sell,
            TradePairORM.average_buy_price: self.average_buy_price,
            TradePairORM.available_quantity: self.available_quantity,
            TradePairORM.first_trade_created_on: self.first_trade_created_on,
            TradePairORM.last_trade_updated_on: self.last_trade_updated_on,
            TradePairORM.trades_updated_on: self.trades_updated_on 
        }
    
    def __repr__(self):
        return f"<TradePair ticker_buy={self.ticker_buy}, ticker_sell={self.ticker_sell}, average_buy_price={self.average_buy_price}, available_quantity={self.available_quantity},  created_on={self.first_trade_created_on}, updated_on={self.last_trade_updated_on}>"

class PairPriceSnapshot:
    def __init__(self, symbol, current_price, created_on, updated_on):
        self.symbol:Symbol = symbol
        self.current_price = current_price
        self.created_on = created_on
        self.updated_on = updated_on
    
    def map_to_orm(self) -> dict:
       return {
           PairPriceSnapshotORM.symbol: self.symbol.with_separator(),
           PairPriceSnapshotORM.current_price: self.current_price,
           PairPriceSnapshotORM.created_on: self.created_on,
           PairPriceSnapshotORM.updated_on: self.updated_on
       }
    
    def __repr__(self):
        return f"<PairPriceSnapshot symbol={self.symbol}, current_price={self.current_price}, created_on={self.created_on}, updated_on={self.updated_on}>"
    
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