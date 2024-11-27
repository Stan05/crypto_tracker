# crypto_tracker/repositories_new/trades_repository.py
from .base_repository import BaseRepository
from .models.base import TradeORM
from sqlalchemy.orm import Session

class TradeRepository(BaseRepository[TradeORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TradeORM)
