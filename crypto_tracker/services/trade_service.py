# crypto_tracker/services/wallet_service.py
from crypto_tracker.database import Database
from crypto_tracker.repositories.models.base import TradeORM


class TradeService:
    def __init__(self):
        self.db = Database()

    def add_trade(self, trade:TradeORM) -> TradeORM:
        return self.db.trade_repo.create(trade)

    def get_trades(self) -> [TradeORM]:
        return self.db.trade_repo.get_all()

    def get_trade(self, trade_id: int) -> TradeORM:
        return self.db.trade_repo.get_by_id(trade_id)
