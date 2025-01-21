# crypto_tracker/repositories/trades_repository.py
from typing import Annotated

from sqlalchemy import func
from wireup import Inject, service

from .base_repository import BaseRepository
from .models.base import TransactionORM
from sqlalchemy.orm import Session

from ..models import TransactionStatusType

@service
class TransactionRepository(BaseRepository[TransactionORM]):
    def __init__(self, db_session: Annotated[Session, Inject()]):
        super().__init__(db_session, TransactionORM)

    def get_txn_by_hash(self, txn_hash: str) -> TransactionORM:
        return (self.db_session
                .query(TransactionORM)
                .filter(func.lower(TransactionORM.hash) == txn_hash.lower())
                .first()
                )

    def update_status_by_id(self, id: int, status: TransactionStatusType) -> None:
        """
        Update the status of a transaction by its ID.

        Args:
            id (int): ID of the transaction to update.
            status (TransactionStatusType): New status to set.

        Returns:
            None
        """
        transaction = (
            self.db_session
            .query(TransactionORM)
            .filter(TransactionORM.id == id)
            .first()
        )
        if transaction:
            transaction.status = status.name
            self.db_session.commit()
        else:
            raise ValueError(f"Transaction with ID {id} not found.")
