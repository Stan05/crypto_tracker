# crypto_tracker/repositories/trades_repository.py
from typing import Annotated

from sqlalchemy import func
from wireup import Inject, service

from .base_repository import BaseRepository
from .models.base import PairORM
from sqlalchemy.orm import Session

@service
class PairRepository(BaseRepository[PairORM]):
    def __init__(self, db_session: Annotated[Session, Inject()]):
        super().__init__(db_session, PairORM)

    def get_pair_by_address(self, address: str) -> PairORM:
        return self.db_session.query(PairORM).filter(func.lower(PairORM.pair_address) == address.lower()).first()
