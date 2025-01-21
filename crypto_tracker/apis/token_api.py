from typing import Self, Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from wireup import Inject

from crypto_tracker.configs.logger import Logger
from ..clients.binance_api_client import BinanceAPIClient
from ..repositories.models.base import TokenORM
from ..services.token_service import TokenService

router = APIRouter()

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
def add_token(request: TokenRequest,
              token_service: Annotated[TokenService, Inject()],
              logger: Annotated[Logger, Inject()]):
    """
    Add a new token.
    """
    logger.info(f"Creating token {request.name} ({request.symbol}) with address {request.address}")
    new_token = token_service.add_token(request.to_orm())
    logger.info(f"Token {request.name} successfully added")
    return TokenResponse.from_orm(new_token)


@router.get("/", response_model=list[TokenResponse])
def get_tokens(token_service: Annotated[TokenService, Inject()],
               logger: Annotated[Logger, Inject()],
               biance: Annotated[BinanceAPIClient, Inject()]):
    """
    Retrieve all tokens.
    """
    tokens = token_service.get_tokens()
    logger.info(f"Retrieved {len(tokens)} tokens")
    biance.fetch_current_price("BTC/USD")
    return [TokenResponse.from_orm(t) for t in tokens]


@router.get("/{token_id}", response_model=TokenResponse)
def get_token(token_id: int,
              token_service: Annotated[TokenService, Inject()],
              logger: Annotated[Logger, Inject()]):
    """
    Retrieve a single token by ID.
    """
    logger.info(f"Fetching token with ID {token_id}")
    token = token_service.get_token(token_id)
    if not token:
        logger.error(f"Token with ID {token_id} not found")
        raise HTTPException(status_code=404, detail="Token not found")
    logger.info(f"Token with ID {token_id} successfully retrieved")
    return TokenResponse.from_orm(token)

