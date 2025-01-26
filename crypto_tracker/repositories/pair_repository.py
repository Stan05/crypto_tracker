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

    def get_pair_by_symbol(self, symbol: str):
        return (self.db_session.query(PairORM)
                .filter(PairORM.symbol == symbol)
                .first())

    def create_with_ignore(self, pair: PairORM) -> PairORM:

        try:
            self.db_session.add(pair)
            self.db_session.commit()
            self.db_session.refresh(pair)
            return pair
        except Exception as e:
            print(f"Exception while creating pair {e}")
            self.db_session.rollback()
            return self.get_pair_by_symbol(pair.symbol)
