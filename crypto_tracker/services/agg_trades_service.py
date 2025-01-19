from typing import List

from wireup import service

from crypto_tracker.database import Database
from crypto_tracker.configs.logger import Logger
from crypto_tracker.models import AggregatedTrade

@service
class AggregatedTradesService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()

    def get_agg_trades(self) -> List[AggregatedTrade]:
        return self.db.trade_repo.get_aggregated_trade_data()


    def get_agg_trade_for_pair(self, pair_id) -> AggregatedTrade:
        return self.db.trade_repo.get_aggregated_trade_data_by_pair_id(pair_id)