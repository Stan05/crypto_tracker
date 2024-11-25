# crypto_tracker/repositories/trade_pair_repository.py

from sqlalchemy.dialects.postgresql import insert
from .base_repository import BaseRepository
from ..models import TradePairORM, TradePair, Symbol
from typing import List
from sqlalchemy import func
from datetime import datetime

class TradePairRepository(BaseRepository):

    def get_trade_pair(self, ticker_buy, ticker_sell) -> TradePair:
        trade_pair: TradePairORM = self.session.query(
            TradePairORM
        ).filter_by(
            ticker_buy=ticker_buy, 
            ticker_sell=ticker_sell
        ).first()
        
        if trade_pair:
            return trade_pair.map_to_model()
        return None
    
    def get_unique_symbols(self) -> List[Symbol]:

        results = self.session.query(
            TradePairORM.ticker_buy, 
            TradePairORM.ticker_sell
        ).all()
        
        symbols: List[Symbol] = []

        for row in results:
            symbols.append(Symbol(
                ticker_buy=row.ticker_buy, 
                ticker_sell=row.ticker_sell)
            )

        return symbols

    def get_trade_pairs(self) -> List[TradePair]:
        query_results: List[TradePairORM] = self.session.query(
            TradePairORM
        ).all()

        trade_pairs: List[TradePair] = []

        for row in query_results:
            trade_pairs.append(row.map_to_model())

        return trade_pairs

    def upsert_trade_pair(self, trade_pair: TradePair):

        stmt = insert(
            TradePairORM
        ).values(
            trade_pair.map_to_orm()
        ).on_conflict_do_update(
            constraint=TradePairORM.ticker_unique_constrant_name(),
            set_={
                TradePairORM.available_quantity: trade_pair.available_quantity,
                TradePairORM.average_buy_price: trade_pair.average_buy_price,
                TradePairORM.last_trade_updated_on: trade_pair.last_trade_updated_on
            }
        )
    
        self.session.execute(stmt)
        self.commit()


    def get_last_trades_updated_on(self, symbol: Symbol) -> datetime:
        # Query the trades_updated_on column and get the first result
        result = self.session.query(
            TradePairORM.trades_updated_on
        ).filter_by(
            ticker_buy=symbol.ticker_buy, 
            ticker_sell=symbol.ticker_sell
        ).first()

        # If result is not None, return the first (and only) element of the tuple, which is updated_on
        return result[0] if result else None  # Return None if no result is found