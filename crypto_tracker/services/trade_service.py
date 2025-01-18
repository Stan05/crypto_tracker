# crypto_tracker/services/wallet_service.py
from wireup import service

from crypto_tracker.database import Database
from crypto_tracker.logger import Logger
from crypto_tracker.repositories.models.base import TradeORM

@service
class TradeService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()

    def add_trade(self, trade:TradeORM) -> TradeORM:
        return self.db.trade_repo.create(trade)

    def add_trade_if_not_exist(self, trade: TradeORM) -> TradeORM:
        existing_trade = self.db.trade_repo.get_trade_by_txn_hash(trade.txn_id)
        if not existing_trade:
            self.logger.info(f'Trade with txn id {trade.txn_id} does not exist creating it')
            return self.db.trade_repo.create(trade)
        return existing_trade

    def get_trades(self) -> [TradeORM]:
        return self.db.trade_repo.get_all()

    def get_trade(self, trade_id: int) -> TradeORM:
        return self.db.trade_repo.get_by_id(trade_id)

    def get_trades_by_pair(self, pair_id: int) -> [TradeORM]:
        return  self.db.trade_repo.get_all_by_pair_id(pair_id)
