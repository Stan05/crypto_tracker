from typing import Any, Self

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..logger import Logger
from crypto_tracker.service_manager import ServiceManager
from ..models import ChainIdType
from ..repositories.models.base import TokenORM

logger = Logger()
router = APIRouter()
service_manager = ServiceManager()


class TokenRequest(BaseModel):
    name: str
    symbol: str
    address: str

    def to_orm(self) -> TokenORM:
        return TokenORM(
            name=self.name,
            symbol=self.symbol,
            address=self.address,
        )

class TokenResponse(BaseModel):
    id: int
    name: str
    symbol: str
    address: str

    @classmethod
    def from_orm(cls, obj: TokenORM) -> Self:
        return TokenResponse(
            id=obj.id,
            name=obj.name,
            symbol=obj.symbol,
            address=obj.address,
        )


@router.post("/", response_model=TokenResponse)
def add_token(request: TokenRequest):
    """
    Add a new token.
    """
    logger.info(f"Creating token {request.name} ({request.symbol}) with address {request.address}")
    new_token = service_manager.token_service.add_token(request.to_orm())
    logger.info(f"Token {request.name} successfully added")
    return TokenResponse.from_orm(new_token)


@router.get("/", response_model=list[TokenResponse])
def get_tokens():
    """
    Retrieve all tokens.
    """
    tokens = service_manager.token_service.get_tokens()
    logger.info(f"Retrieved {len(tokens)} tokens")
    return [TokenResponse.from_orm(t) for t in tokens]


@router.get("/{token_id}", response_model=TokenResponse)
def get_token(token_id: int):
    """
    Retrieve a single token by ID.
    """
    logger.info(f"Fetching token with ID {token_id}")
    token = service_manager.token_service.get_token(token_id)
    if not token:
        logger.error(f"Token with ID {token_id} not found")
        raise HTTPException(status_code=404, detail="Token not found")
    logger.info(f"Token with ID {token_id} successfully retrieved")
    return TokenResponse.from_orm(token)

