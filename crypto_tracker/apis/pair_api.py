from typing import Any, Self

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..logger import Logger
from crypto_tracker.service_manager import ServiceManager
from ..models_new import ChainIdType, DexIdType
from ..repositories_new.models.base import PairORM

logger = Logger()
router = APIRouter()
service_manager = ServiceManager()

class PairRequest(BaseModel):
    symbol: str
    base_token_id: int
    quote_token_id: int
    chain_id: ChainIdType
    dex_id: DexIdType
    pair_address: str
    def to_orm(self) -> PairORM:
        return PairORM(
            symbol=self.symbol,
            base_token_id=self.base_token_id,
            quote_token_id=self.quote_token_id,
            chain_id=self.chain_id.name,
            dex_id=self.dex_id.name,
            pair_address=self.pair_address,
        )


class PairResponse(BaseModel):
    id: int
    symbol: str
    base_token_id: int
    quote_token_id: int
    chain_id: str
    dex_id: str
    pair_address: str

    @classmethod
    def from_orm(cls, obj: PairORM) -> Self:
        return PairResponse(
            id=obj.id,
            symbol=obj.symbol,
            base_token_id=obj.base_token_id,
            quote_token_id=obj.quote_token_id,
            chain_id=obj.chain_id,
            dex_id=obj.dex_id,
            pair_address=obj.pair_address,
        )


@router.post("/pairs", response_model=PairResponse)
def add_pair(request: PairRequest):
    """
    Add a new pair.
    """
    logger.info(f"Creating pair {request.symbol} on chain {request.chain_id}")
    new_pair = service_manager.pair_service.add_pair(request.to_orm())
    logger.info(f"Pair {request.symbol} successfully added")
    return PairResponse.from_orm(new_pair)


@router.get("/pairs", response_model=list[PairResponse])
def get_pairs():
    """
    Retrieve all pairs.
    """
    pairs = service_manager.pair_service.get_pairs()
    logger.info(f"Retrieved {len(pairs)} pairs")
    return [PairResponse.from_orm(p) for p in pairs]


@router.get("/pairs/{pair_id}", response_model=PairResponse)
def get_pair(pair_id: int):
    """
    Retrieve a single pair by ID.
    """
    logger.info(f"Fetching pair with ID {pair_id}")
    pair = service_manager.pair_service.get_pair(pair_id)
    if not pair:
        logger.error(f"Pair with ID {pair_id} not found")
        raise HTTPException(status_code=404, detail="Pair not found")
    logger.info(f"Pair with ID {pair_id} successfully retrieved")
    return PairResponse.from_orm(pair)
