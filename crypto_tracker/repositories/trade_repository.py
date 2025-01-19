# crypto_tracker/repositories/trades_repository.py
from sqlalchemy import func, case

from .base_repository import BaseRepository
from .models.base import TradeORM, PairORM
from sqlalchemy.orm import Session

from crypto_tracker.configs.logger import Logger
from ..models import TradeType, AggregatedTrade


class TradeRepository(BaseRepository[TradeORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, TradeORM)
        self.logger = Logger()

    def create(self, obj: TradeORM) -> TradeORM:
        """Override create to handle trade-specific logic."""
        if obj.trade_type == TradeType.SELL:
            obj.quantity = -abs(obj.quantity)  # Ensure quantity is negative for sells
        elif obj.trade_type == TradeType.BUY:
            obj.quantity = abs(obj.quantity)  # Ensure quantity is positive for buys

        # Call the base class create method
        return super().create(obj)

    def get_trade_by_txn_hash(self, txn_id: str) -> TradeORM:
        return (self.db_session
                .query(TradeORM)
                .filter(TradeORM.txn_id == txn_id)
                .first()
                )

    def get_all_by_pair_id(self, pair_id: int) -> [TradeORM]:
        return (self.db_session
                .query(TradeORM)
                .filter(TradeORM.pair_id == pair_id)
                .order_by(TradeORM.trade_timestamp)
                .all())

    def get_aggregated_trade_data_by_pair_id(self, pair_id: int):
        query = (
            self.__get_aggregated_trade_date_query()
            .join(PairORM, PairORM.id == TradeORM.pair_id)
            .where(PairORM.id == pair_id)
            .group_by(PairORM.id, PairORM.symbol)
        )

        # Execute the query
        result = query.first()

        # Map results to AggregatedTrade
        return AggregatedTrade(
                pair_id=result.id,
                pair=result.pair,
                total_buy_quantity=result.total_buy_quantity,
                total_buy_native_value=result.total_buy_native_value,
                total_buy_usd_value=result.total_buy_usd_value,
                total_sell_quantity=result.total_sell_quantity,
                total_sell_native_value=result.total_sell_native_value,
                total_sell_usd_value=result.total_sell_usd_value,
            )

    def get_aggregated_trade_data(self):
        query = (
            self.__get_aggregated_trade_date_query()
            .join(PairORM, PairORM.id == TradeORM.pair_id)
            .group_by(PairORM.id, PairORM.symbol)
        )

        # Execute the query
        results = query.all()

        # Map results to AggregatedTrade
        return [
            AggregatedTrade(
                pair_id=row.id,
                pair=row.pair,
                total_buy_quantity=row.total_buy_quantity,
                total_buy_native_value=row.total_buy_native_value,
                total_buy_usd_value=row.total_buy_usd_value,
                total_sell_quantity=row.total_sell_quantity,
                total_sell_native_value=row.total_sell_native_value,
                total_sell_usd_value=row.total_sell_usd_value,
            )
            for row in results
        ]

    def __get_aggregated_trade_date_query(self):
        return self.db_session.query(
            PairORM.id,
            PairORM.symbol.label("pair"),
            func.sum(
                case((TradeORM.trade_type == TradeType.BUY.name, TradeORM.quantity), else_=0)
            ).label("total_buy_quantity"),
            func.sum(
                case((TradeORM.trade_type == TradeType.BUY.name, TradeORM.native_price * TradeORM.quantity),
                     else_=0)
            ).label("total_buy_native_value"),
            func.sum(
                case((TradeORM.trade_type == TradeType.BUY.name, TradeORM.usd_price * TradeORM.quantity), else_=0)
            ).label("total_buy_usd_value"),
            func.abs(
                func.sum(
                    case((TradeORM.trade_type == TradeType.SELL.name, TradeORM.quantity), else_=0)
                )
            ).label("total_sell_quantity"),
            func.abs(
                func.sum(
                    case((TradeORM.trade_type == TradeType.SELL.name, TradeORM.native_price * TradeORM.quantity),
                         else_=0)
                )
            ).label("total_sell_native_value"),
            func.abs(
                func.sum(
                    case((TradeORM.trade_type == TradeType.SELL.name, TradeORM.usd_price * TradeORM.quantity), else_=0)
                )
            ).label("total_sell_usd_value"),
        )