# crypto_tracker/repositories/trades_repository.py
from sqlalchemy import exists, func

from .base_repository import BaseRepository
from .models.base import TokenORM
from sqlalchemy.orm import Session

class TokenRepository(BaseRepository[TokenORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TokenORM)

    def get_token_by_address(self, address: str) -> TokenORM:
        return self.db_session.query(TokenORM).filter(func.lower(TokenORM.address) == address.lower()).first()