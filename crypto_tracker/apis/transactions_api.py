from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel
from wireup import Inject

from crypto_tracker.configs.logger import Logger
from ..models import ChainIdType, DexIdType
from ..services.transaction_service import TransactionService

router = APIRouter()

class QueryTxnRequest(BaseModel):
    txn_id: str
    chain_id: ChainIdType
    dex_id: DexIdType

class QueryTxnResponse(BaseModel):
    id: int


@router.post("/", response_model=QueryTxnResponse)
def process_transaction(request: QueryTxnRequest,
                        transaction_service: Annotated[TransactionService, Inject()],
                        logger: Annotated[Logger, Inject()]):
    """
    Add a new trade.
    """
    logger.info(f"Querying txn {request.txn_id} on chain {request.chain_id} from dex {request.dex_id}")
    transaction_service.process_transaction(request.txn_id, request.chain_id, request.dex_id)
    logger.info("Transaction successfully processed")
    return QueryTxnResponse(id=1)


