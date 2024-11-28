# crypto_tracker/services/wallet_service.py
from crypto_tracker.database import Database
from crypto_tracker.repositories_new.models.base import TradeORM, PairORM


class PairService:
    def __init__(self):
        self.db = Database()

    def add_pair(self, pair:PairORM) -> PairORM:
        return self.db.trade_repo.create(pair)

    def get_pairs(self) -> [PairORM]:
        return self.db.trade_repo.get_all()

    def get_pair(self, trade_id: int) -> PairORM:
        return self.db.trade_repo.get_by_id(trade_id)
