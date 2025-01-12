from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from crypto_tracker.service_manager import ServiceManager
from ..logger import Logger
from ..models import TradeStatus, AggregatedTrade

logger = Logger()
router = APIRouter()
service_manager = ServiceManager()

class AggTrade(BaseModel):
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

class AggTradesResponse(BaseModel):
    agg_trades: List[AggTrade]

@router.get("/", response_model=AggTradesResponse)
def add_pair():
    """
    Retrieve aggregated trades.
    """
    logger.info(f"Retrieving aggregated trades")
    agg_trades:List[AggregatedTrade] = service_manager.agg_trades_service.get_agg_trades()
    logger.info(f'Agg trades {agg_trades}')

    agg_trades_response = []
    for agg_trade in agg_trades:
        available_quantity = agg_trade.total_bought_quantity - agg_trade.total_sold_quantity

        # Calculate PNL
        total_investment_native = agg_trade.total_bought_quantity * agg_trade.average_buy_native_price
        total_investment_USD = agg_trade.total_bought_quantity * agg_trade.average_buy_USD_price

        total_sold_native = agg_trade.total_sold_quantity * agg_trade.average_sell_native_price
        total_sold_USD = agg_trade.total_sold_quantity * agg_trade.average_sell_USD_price

        pnl_native = total_sold_native - total_investment_native
        pnl_USD = total_sold_USD - total_investment_USD
        pnl_percent = (pnl_USD / total_investment_USD * 100) if total_investment_USD > 0 else 0

        # Determine status
        if available_quantity > 0:
            if total_sold_USD >= total_investment_USD:
                status = TradeStatus.MOON_BAG
            else:
                status = TradeStatus.IN_TRADE
        else:
            status = TradeStatus.SOLD

        # Add to response
        agg_trades_response.append(
            AggTrade(
                pair=agg_trade.pair,
                available_quantity=available_quantity,

                total_bought_quantity=agg_trade.total_bought_quantity,
                average_buy_native_price=agg_trade.average_buy_native_price,
                average_buy_USD_price=agg_trade.average_buy_USD_price,

                total_sold_quantity=agg_trade.total_sold_quantity,
                average_sell_native_price=agg_trade.average_sell_native_price,
                average_sell_USD_price=agg_trade.average_sell_USD_price,

                pnl_percent=pnl_percent,
                pnl_native=pnl_native,
                pnl_USD=pnl_USD,

                status=status,
            )
        )

    return AggTradesResponse(agg_trades=agg_trades_response)

@router.get("/{pair_id}", response_model=AggTrade)
def get_pair(pair_id: int):
    """
    Retrieve a single aggregated trade by ID.
    """
    logger.info(f"Fetching aggregated trade for pair with ID {pair_id}")
    agg_trade = service_manager.agg_trades_service.get_agg_trade(pair_id)

    if not agg_trade:
        logger.error(f"Pair with ID {pair_id} not found")
        raise HTTPException(status_code=404, detail="Pair not found")

    return AggTrade.model_validate(agg_trade)

