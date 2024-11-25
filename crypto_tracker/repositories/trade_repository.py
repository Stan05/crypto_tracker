# crypto_tracker/repositories/trade_repository.py

from sqlalchemy.dialects.postgresql import insert
from .base_repository import BaseRepository
from ..models import TradeORM, Trade, Symbol

class TradeRepository(BaseRepository):
    
    def upsert_trade(self, trade: Trade):
    
        stmt = insert(TradeORM).values(
            trade.map_to_orm()
        ).on_conflict_do_update(
            constraint=TradeORM.order_id_unique_constraint_name(),
            set_={
                TradeORM.status: trade.status,
                TradeORM.updated_on: trade.updated_on
            }
        )
    
        self.session.execute(stmt)
        self.commit()

    def get_trades(self, symbol:Symbol, status:str):

        trades = self.session.query(
            TradeORM
        ).filter_by(
            symbol=symbol.with_separator(), 
            status=status
        ).all()

        return [Trade(
                    order_id=trade.order_id,
                    symbol=trade.symbol,
                    price=trade.price,
                    qty=trade.qty,
                    side=trade.side,
                    status=trade.status,
                    platform=trade.platform,
                    created_on=trade.created_on,
                    updated_on=trade.updated_on
                ) for trade in trades]
