# crypto_tracker/repositories/trades_repository.py
from .base_repository import BaseRepository
from .models.base import PriceSnapshotORM
from sqlalchemy.orm import Session

class PriceSnapshotRepository(BaseRepository[PriceSnapshotORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, PriceSnapshotORM)

