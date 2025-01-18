from typing import List, Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from wireup import Inject

from .trades_api import TradeResponse
from ..logger import Logger
from ..models import TradeStatus, AggregatedTrade
from ..services.agg_trades_service import AggregatedTradesService
from ..services.trade_service import TradeService

logger = Logger()
router = APIRouter()

class AggTradeResponse(BaseModel):
    pair_id: int
    pair: str
    available_quantity: float

    total_bought_quantity: float
    average_buy_native_price: float
    average_buy_USD_price: float

    total_sold_quantity: float
    average_sell_native_price: float
    average_sell_USD_price: float

    pnl_percent: float
    pnl_native: float
    pnl_USD: float

    status: TradeStatus
    trades: List[TradeResponse]

class AggTradesResponse(BaseModel):
    agg_trades: List[AggTradeResponse]

@router.get("/", response_model=AggTradesResponse)
def add_pair(agg_trades_service: Annotated[AggregatedTradesService, Inject()]):
    """
    Retrieve aggregated trades.
    """
    logger.info(f"Retrieving aggregated trades")
    agg_trades:List[AggregatedTrade] = agg_trades_service.get_agg_trades()
    logger.info(f'Agg trades {agg_trades}')

    agg_trades_response = []
    for raw_trade in agg_trades:
        # Extract raw values
        pair = raw_trade.pair
        total_buy_quantity = raw_trade.total_buy_quantity
        total_buy_native_value = raw_trade.total_buy_native_value
        total_buy_usd_value = raw_trade.total_buy_usd_value
        total_sell_quantity = raw_trade.total_sell_quantity
        total_sell_native_value = raw_trade.total_sell_native_value
        total_sell_usd_value = raw_trade.total_sell_usd_value

        # Avoid division by zero
        average_buy_native_price = (
            total_buy_native_value / total_buy_quantity
            if total_buy_quantity > 0
            else 0
        )
        average_buy_usd_price = (
            total_buy_usd_value / total_buy_quantity
            if total_buy_quantity > 0
            else 0
        )
        average_sell_native_price = (
            total_sell_native_value / total_sell_quantity
            if total_sell_quantity > 0
            else 0
        )
        average_sell_usd_price = (
            total_sell_usd_value / total_sell_quantity
            if total_sell_quantity > 0
            else 0
        )

        # Calculate PNL
        pnl_native = total_sell_native_value - total_buy_native_value if total_sell_usd_value > 0 else 0
        pnl_usd = total_sell_usd_value - total_buy_usd_value if total_sell_usd_value > 0 else 0
        pnl_percent = (
            (pnl_usd / total_buy_usd_value) * 100 if total_buy_usd_value > 0 and pnl_usd > 0 else 0
        )

        # Determine status
        available_quantity = total_buy_quantity - total_sell_quantity
        if available_quantity > 0:
            if total_sell_usd_value >= total_buy_usd_value:
                status = TradeStatus.MOON_BAG
            else:
                status = TradeStatus.IN_TRADE
        else:
            status = TradeStatus.SOLD

        # Add to response
        agg_trades_response.append(
            AggTradeResponse(
                pair_id=raw_trade.pair_id,
                pair=pair,
                available_quantity=available_quantity,

                total_bought_quantity=total_buy_quantity,
                average_buy_native_price=average_buy_native_price,
                average_buy_USD_price=average_buy_usd_price,

                total_sold_quantity=total_sell_quantity,
                average_sell_native_price=average_sell_native_price,
                average_sell_USD_price=average_sell_usd_price,

                pnl_percent=pnl_percent,
                pnl_native=pnl_native,
                pnl_USD=pnl_usd,

                status=status,
                trades=[]
            )
        )

    return AggTradesResponse(agg_trades=agg_trades_response)

@router.get("/{pair_id}", response_model=AggTradeResponse)
def get_pair_details(pair_id: int,
                     agg_trades_service: Annotated[AggregatedTradesService, Inject()],
                     trade_service: Annotated[TradeService, Inject()]):
    """
    Retrieve aggregated data and all trades for a specific pair.
    """
    # Fetch aggregated data for the pair
    aggregated_data:AggregatedTrade = agg_trades_service.get_agg_trade_for_pair(pair_id)
    if not aggregated_data:
        raise HTTPException(status_code=404, detail="Pair not found")

    # Fetch all trades for the pair
    trades = trade_service.get_trades_by_pair(pair_id)
    logger.info(aggregated_data)
    # Extract raw values
    pair = aggregated_data.pair
    total_buy_quantity = aggregated_data.total_buy_quantity
    total_buy_native_value = aggregated_data.total_buy_native_value
    total_buy_usd_value = aggregated_data.total_buy_usd_value
    total_sell_quantity = aggregated_data.total_sell_quantity
    total_sell_native_value = aggregated_data.total_sell_native_value
    total_sell_usd_value = aggregated_data.total_sell_usd_value

    # Avoid division by zero
    average_buy_native_price = (
        total_buy_native_value / total_buy_quantity
        if total_buy_quantity > 0
        else 0
    )
    average_buy_usd_price = (
        total_buy_usd_value / total_buy_quantity
        if total_buy_quantity > 0
        else 0
    )
    average_sell_native_price = (
        total_sell_native_value / total_sell_quantity
        if total_sell_quantity > 0
        else 0
    )
    average_sell_usd_price = (
        total_sell_usd_value / total_sell_quantity
        if total_sell_quantity > 0
        else 0
    )

    # Calculate PNL
    pnl_native = total_sell_native_value - total_buy_native_value
    pnl_usd = total_sell_usd_value - total_buy_usd_value
    pnl_percent = (
        (pnl_usd / total_buy_usd_value) * 100 if total_buy_usd_value > 0 else 0
    )

    # Determine status
    available_quantity = total_buy_quantity - total_sell_quantity
    if available_quantity > 0:
        if total_sell_usd_value >= total_buy_usd_value:
            status = TradeStatus.MOON_BAG
        else:
            status = TradeStatus.IN_TRADE
    else:
        status = TradeStatus.SOLD

    return AggTradeResponse(
        pair_id=aggregated_data.pair_id,
        pair=pair,
        available_quantity=available_quantity,

        total_bought_quantity=total_buy_quantity,
        average_buy_native_price=average_buy_native_price,
        average_buy_USD_price=average_buy_usd_price,

        total_sold_quantity=total_sell_quantity,
        average_sell_native_price=average_sell_native_price,
        average_sell_USD_price=average_sell_usd_price,

        pnl_percent=pnl_percent,
        pnl_native=pnl_native,
        pnl_USD=pnl_usd,

        status=status,
        trades=[
            TradeResponse.from_orm(trade)
            for trade in trades
        ]
    )

