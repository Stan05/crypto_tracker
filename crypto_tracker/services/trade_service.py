# crypto_tracker/services/wallet_service.py
from typing import Annotated

from wireup import service, Inject

from crypto_tracker.configs.logger import Logger
from crypto_tracker.repositories.models.base import TradeORM
from crypto_tracker.repositories.trade_repository import TradeRepository


@service
class TradeService:
    def __init__(self,
                 trade_repo: Annotated[TradeRepository, Inject()],
                 logger: Annotated[Logger, Inject()],):
        self.trade_repo = trade_repo
        self.logger = logger

    def add_trade(self, trade:TradeORM) -> TradeORM:
        return self.trade_repo.create(trade)

    def add_trade_if_not_exist(self, trade: TradeORM) -> TradeORM:
        existing_trade = self.trade_repo.get_trade_by_txn_hash(trade.txn_id)
        if not existing_trade:
            self.logger.info(f'Trade with txn id {trade.txn_id} does not exist creating it')
            return self.trade_repo.create(trade)
        return existing_trade

    def get_trades(self) -> [TradeORM]:
        return self.trade_repo.get_all()

    def get_trade(self, trade_id: int) -> TradeORM:
        return self.trade_repo.get_by_id(trade_id)

    def get_trades_by_pair(self, pair_id: int) -> [TradeORM]:
        return  self.trade_repo.get_all_by_pair_id(pair_id)
