from typing import Any, Self, Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from wireup import Inject

from ..logger import Logger
from ..models import ChainIdType, DexIdType
from ..repositories.models.base import PairORM
from ..services.pair_service import PairService

logger = Logger()
router = APIRouter()

class PairRequest(BaseModel):

    base_token_id: int
    quote_token_id: int
    chain_id: ChainIdType
    dex_id: DexIdType
    pair_address: str

    def to_orm(self) -> PairORM:
        return PairORM(
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


@router.post("/", response_model=PairResponse)
def add_pair(request: PairRequest, pair_service: Annotated[PairService, Inject()]):
    """
    Add a new pair.
    """
    logger.info(f"Creating pair on chain {request.chain_id}")
    new_pair = pair_service.add_pair(request.to_orm())
    logger.info(f"Pair {new_pair.symbol} successfully added")
    return PairResponse.from_orm(new_pair)


@router.get("/", response_model=list[PairResponse])
def get_pairs(pair_service: Annotated[PairService, Inject()]):
    """
    Retrieve all pairs.
    """
    pairs = pair_service.get_pairs()
    logger.info(f"Retrieved {len(pairs)} pairs")
    return [PairResponse.from_orm(p) for p in pairs]


@router.get("/{pair_id}", response_model=PairResponse)
def get_pair(pair_id: int, pair_service: Annotated[PairService, Inject()]):
    """
    Retrieve a single pair by ID.
    """
    logger.info(f"Fetching pair with ID {pair_id}")
    pair = pair_service.get_pair(pair_id)
    if not pair:
        logger.error(f"Pair with ID {pair_id} not found")
        raise HTTPException(status_code=404, detail="Pair not found")
    logger.info(f"Pair with ID {pair_id} successfully retrieved")
    return PairResponse.from_orm(pair)

