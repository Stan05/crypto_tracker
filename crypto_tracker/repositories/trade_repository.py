# crypto_tracker/repositories/trades_repository.py
from sqlalchemy import func, case

from .base_repository import BaseRepository
from .models.base import TradeORM, PairORM
from sqlalchemy.orm import Session

from crypto_tracker.logger import Logger
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

    def get_aggregated_trade_data(self):
        query = (
            self.db_session.query(
                PairORM.symbol.label("pair"),
                # Calculate Buy Quantities
                func.sum(
                    case((TradeORM.trade_type == TradeType.BUY.name, TradeORM.quantity), else_=0)
                ).label("buy_quantity"),
                # Average Buy Native Price
                (
                        func.sum(
                            case((TradeORM.trade_type == TradeType.BUY.name, TradeORM.native_price * TradeORM.quantity),
                                 else_=0)
                        ) / func.sum(
                    case((TradeORM.trade_type == TradeType.BUY.name, TradeORM.quantity), else_=0)
                )
                ).label("avg_buy_native_price"),
                # Average Buy USD Price
                (
                        func.sum(
                            case((TradeORM.trade_type == TradeType.BUY.name, TradeORM.usd_price * TradeORM.quantity),
                                 else_=0)
                        ) / func.sum(
                    case((TradeORM.trade_type == TradeType.BUY.name, TradeORM.quantity), else_=0)
                )
                ).label("avg_buy_usd_price"),
                # Calculate Sell Quantities
                func.abs(
                    func.sum(
                        case((TradeORM.trade_type == TradeType.SELL.name, TradeORM.quantity), else_=0)
                    )
                ).label("sell_quantity"),
                # Average Sell Native Price
                (
                        func.sum(
                            case(
                                (TradeORM.trade_type == TradeType.SELL.name, TradeORM.native_price * TradeORM.quantity),
                                else_=0)
                        ) / func.sum(
                    case((TradeORM.trade_type == TradeType.SELL.name, TradeORM.quantity), else_=0)
                )
                ).label("avg_sell_native_price"),
                # Average Sell USD Price
                (
                        func.sum(
                            case((TradeORM.trade_type == TradeType.SELL.name, TradeORM.usd_price * TradeORM.quantity),
                                 else_=0)
                        ) / func.sum(
                    case((TradeORM.trade_type == TradeType.SELL.name, TradeORM.quantity), else_=0)
                )
                ).label("avg_sell_usd_price"),
            )
            .join(PairORM, PairORM.id == TradeORM.pair_id)
            .group_by(PairORM.symbol)
        )

        # Execute the query
        results = query.all()

        # Map results to AggregatedTrade
        return [
            AggregatedTrade(
                pair=row.pair,
                total_bought_quantity=row.buy_quantity,
                average_buy_native_price=row.avg_buy_native_price,
                average_buy_USD_price=row.avg_buy_usd_price,
                total_sold_quantity=row.sell_quantity,
                average_sell_native_price=row.avg_sell_native_price,
                average_sell_USD_price=row.avg_sell_usd_price,
            )
            for row in results
        ]