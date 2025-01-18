from typing import Any, Self, Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from wireup import Inject

from ..logger import Logger
from ..repositories.models.base import TokenORM
from ..services.token_service import TokenService

logger = Logger()
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
def add_token(request: TokenRequest, token_service: Annotated[TokenService, Inject()]):
    """
    Add a new token.
    """
    logger.info(f"Creating token {request.name} ({request.symbol}) with address {request.address}")
    new_token = token_service.add_token(request.to_orm())
    logger.info(f"Token {request.name} successfully added")
    return TokenResponse.from_orm(new_token)


@router.get("/", response_model=list[TokenResponse])
def get_tokens(token_service: Annotated[TokenService, Inject()]):
    """
    Retrieve all tokens.
    """
    tokens = token_service.get_tokens()
    logger.info(f"Retrieved {len(tokens)} tokens")
    return [TokenResponse.from_orm(t) for t in tokens]


@router.get("/{token_id}", response_model=TokenResponse)
def get_token(token_id: int, token_service: Annotated[TokenService, Inject()]):
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

