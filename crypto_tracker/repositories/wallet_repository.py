# crypto_tracker/repositories/trades_repository.py
from sqlalchemy import and_, func

from .base_repository import BaseRepository
from .models.base import WalletORM
from sqlalchemy.orm import Session

from ..models import ChainIdType

class WalletRepository(BaseRepository[WalletORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, WalletORM)

    def get_wallet_by_address_and_chain(self, address: str, chain_id: ChainIdType) -> WalletORM:
        return (self.db_session
                .query(WalletORM)
                .filter(and_(func.lower(WalletORM.address) == address.lower(),
                             WalletORM.chain_id == chain_id.name))
                .first()
                )
