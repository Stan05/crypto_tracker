# crypto_tracker/repositories/trades_repository.py
from typing import Annotated

from wireup import Inject, service

from .base_repository import BaseRepository
from .models.base import PriceSnapshotORM
from sqlalchemy.orm import Session

@service
class PriceSnapshotRepository(BaseRepository[PriceSnapshotORM]):
    def __init__(self, db_session: Annotated[Session, Inject()]):
        super().__init__(db_session, PriceSnapshotORM)

