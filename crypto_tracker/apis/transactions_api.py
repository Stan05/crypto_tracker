
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..logger import Logger
from crypto_tracker.service_manager import ServiceManager
from ..models import TradeType, ChainIdType, DexIdType

logger = Logger()
router = APIRouter()
service_manager = ServiceManager()

class QueryTxnRequest(BaseModel):
    txn_id: str
    chain_id: ChainIdType
    dex_id: DexIdType

class QueryTxnResponse(BaseModel):
    id: int
    pair_id: int
    trade_type: str
    native_price: float
    usd_price: float
    quantity: float
    trade_timestamp: str
    wallet_id: int


@router.post("/", response_model=QueryTxnResponse)
def query_transaction(request: QueryTxnRequest):
    """
    Add a new trade.
    """
    logger.info(f"Querying txn {request.txn_id} on chain {request.chain_id} from dex {request.dex_id}")
    queried_txn = service_manager.transaction_service.query_txn(request.txn_id, request.chain_id, request.dex_id)
    logger.info(f"Trade successfully added with ID {queried_txn.id}")
    return queried_txn


