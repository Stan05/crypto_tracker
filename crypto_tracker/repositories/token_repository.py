# crypto_tracker/repositories/trades_repository.py
from sqlalchemy import exists

from .base_repository import BaseRepository
from .models.base import TokenORM
from sqlalchemy.orm import Session

class TokenRepository(BaseRepository[TokenORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TokenORM)

    def exists(self, address: str) -> bool:
        return self.db_session.query(exists().where(TokenORM.address == address)).scalar()