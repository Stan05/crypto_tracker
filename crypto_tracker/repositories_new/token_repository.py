# crypto_tracker/repositories_new/trades_repository.py
from .base_repository import BaseRepository
from .models.base import TokenORM
from sqlalchemy.orm import Session

class TokenRepository(BaseRepository[TokenORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TokenORM)

