# crypto_tracker/repositories/trades_repository.py
from sqlalchemy import func

from .base_repository import BaseRepository
from .models.base import TradeORM
from sqlalchemy.orm import Session

class TradeRepository(BaseRepository[TradeORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TradeORM)

    def get_trade_by_txn_hash(self, txn_id: str) -> TradeORM:
        return (self.db_session
                .query(TradeORM)
                .filter(TradeORM.txn_id == txn_id)
                .first()
                )
