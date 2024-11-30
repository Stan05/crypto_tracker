# crypto_tracker/repositories/trades_repository.py
from .base_repository import BaseRepository
from .models.base import WalletORM
from sqlalchemy.orm import Session

class WalletRepository(BaseRepository[WalletORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, WalletORM)

