from typing import List

from crypto_tracker.database import Database
from crypto_tracker.logger import Logger
from crypto_tracker.models import AggregatedTrade


class AggregatedTradesService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()

    def get_agg_trades(self) -> List[AggregatedTrade]:
        return self.db.trade_repo.get_aggregated_trade_data()


    def get_agg_trade(self, pair_id) -> AggregatedTrade:
        return AggregatedTrade()