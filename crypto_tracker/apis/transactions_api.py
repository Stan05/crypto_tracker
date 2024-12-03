
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


@router.post("/", response_model=QueryTxnResponse)
def process_transaction(request: QueryTxnRequest):
    """
    Add a new trade.
    """
    logger.info(f"Querying txn {request.txn_id} on chain {request.chain_id} from dex {request.dex_id}")
    service_manager.transaction_service.process_transaction(request.txn_id, request.chain_id, request.dex_id)
    logger.info("Transaction successfully processed")
    return QueryTxnResponse(id=1)



