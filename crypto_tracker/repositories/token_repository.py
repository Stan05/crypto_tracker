# crypto_tracker/repositories/trades_repository.py
from typing import Annotated

from sqlalchemy import func
from wireup import Inject, service

from .base_repository import BaseRepository
from .models.base import TokenORM
from sqlalchemy.orm import Session

@service
class TokenRepository(BaseRepository[TokenORM]):
    def __init__(self, db_session: Annotated[Session, Inject()]):
        super().__init__(db_session, TokenORM)

    def get_token_by_address(self, address: str) -> TokenORM:
        return self.db_session.query(TokenORM).filter(func.lower(TokenORM.address) == address.lower()).first()