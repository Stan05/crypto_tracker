from typing import List, Annotated

from wireup import service, Inject

from crypto_tracker.models import AggregatedTrade
from crypto_tracker.repositories.trade_repository import TradeRepository


@service
class AggregatedTradesService:
    def __init__(self, trade_repo: Annotated[TradeRepository, Inject()]):
        self.trade_repo = trade_repo

    def get_agg_trades(self) -> List[AggregatedTrade]:
        return self.trade_repo.get_aggregated_trade_data()


    def get_agg_trade_for_pair(self, pair_id) -> AggregatedTrade:
        return self.trade_repo.get_aggregated_trade_data_by_pair_id(pair_id)