from datetime import datetime
from typing import Any, Self

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..logger import Logger
from crypto_tracker.service_manager import ServiceManager
from ..models import TradeType
from ..repositories.models.base import TradeORM

logger = Logger()
router = APIRouter()
service_manager = ServiceManager()

class TradeRequest(BaseModel):
    pair_id: int
    trade_type: TradeType
    native_price: float
    usd_price: float
    quantity: float
    trade_timestamp: datetime
    wallet_id: int

    def to_orm(self) -> TradeORM:
        return TradeORM(
            pair_id=self.pair_id,
            trade_type=self.trade_type.name,
            native_price=self.native_price,
            usd_price=self.usd_price,
            quantity=self.quantity,
            trade_timestamp=self.trade_timestamp,
            wallet=self.wallet_id,
        )

class TradeResponse(BaseModel):
    id: int
    pair_id: int
    trade_type: str
    native_price: float
    usd_price: float
    quantity: float
    trade_timestamp: str
    wallet_id: int

    @classmethod
    def from_orm(cls, obj: TradeORM) -> Self:
        return TradeResponse(
            id=obj.id,
            pair_id=obj.pair_id,
            trade_type=obj.trade_type,
            native_price=obj.native_price,
            usd_price=obj.usd_price,
            quantity=obj.quantity,
            trade_timestamp=obj.trade_timestamp.isoformat(),
            wallet_id=obj.wallet,
        )


@router.post("/", response_model=TradeResponse)
def add_trade(request: TradeRequest):
    """
    Add a new trade.
    """
    logger.info(f"Adding trade for pair_id {request.pair_id} with trade_type {request.trade_type}")
    new_trade = service_manager.trade_service.add_trade(request.to_orm())
    logger.info(f"Trade successfully added with ID {new_trade.id}")
    return TradeResponse.from_orm(new_trade)


@router.get("/", response_model=list[TradeResponse])
def get_trades():
    """
    Retrieve all trades.
    """
    trades = service_manager.trade_service.get_trades()
    logger.info(f"Retrieved {len(trades)} trades")
    return [TradeResponse.from_orm(t) for t in trades]


@router.get("/{trade_id}", response_model=TradeResponse)
def get_trade(trade_id: int):
    """
    Retrieve a single trade by ID.
    """
    logger.info(f"Fetching trade with ID {trade_id}")
    trade = service_manager.trade_service.get_trade(trade_id)
    if not trade:
        logger.error(f"Trade with ID {trade_id} not found")
        raise HTTPException(status_code=404, detail="Trade not found")
    logger.info(f"Trade with ID {trade_id} successfully retrieved")
    return TradeResponse.from_orm(trade)

