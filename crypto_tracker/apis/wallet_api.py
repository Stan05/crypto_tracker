from typing import Any, Self, Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from wireup import Inject

from ..logger import Logger
from ..models import ChainIdType
from ..repositories.models.base import WalletORM
from ..services.wallet_service import WalletService

logger = Logger()
router = APIRouter()

class WalletRequest(BaseModel):
    address: str
    chain_id: str
    name: str

class WalletResponse(BaseModel):
    id: int
    name: str
    address: str
    chain_id: str

    @classmethod
    def from_orm(cls, obj: WalletORM) -> Self:
        return WalletResponse(id=obj.id, name=obj.name, address=obj.address, chain_id=obj.chain_id)


@router.post("/", response_model=WalletResponse)
def add_wallet(request: WalletRequest, wallet_service: Annotated[WalletService, Inject()]):
    """
    Add a new wallet.
    """
    """
    # Check if the wallet already exists
    if wallet_repo.get_by_address(request.address):
        raise HTTPException(status_code=400, detail="Wallet already exists")
    """
    # Add the wallet
    logger.info(f"Creating wallet with name {request.name} for chain {request.chain_id} with address {request.address}")
    new_wallet = wallet_service.add_wallet(wallet_address=request.address, chain_id=ChainIdType.from_name(request.chain_id), name=request.name)
    logger.info(f"Wallet successfully added")
    return WalletResponse.from_orm(new_wallet)


@router.get("/", response_model=list[WalletResponse])
def get_wallets(wallet_service: Annotated[WalletService, Inject()]):
    """
    Retrieve all wallets.
    """
    wallets = wallet_service.get_wallets()
    return [WalletResponse.from_orm(w) for w in wallets]


@router.get("/{wallet_id}", response_model=WalletResponse)
def get_wallet(wallet_id: int, wallet_service: Annotated[WalletService, Inject()]):
    """
    Retrieve a single wallet by ID.
    """
    wallet = wallet_service.get_wallet(wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletResponse.from_orm(wallet)

"""
@router.delete("/wallets/{wallet_id}")
def delete_wallet(wallet_id: int, db: Session = Depends(get_db)):
    \"""
    Delete a wallet by ID.
    \"""
    wallet_repo = WalletRepository(db)
    wallet = wallet_repo.get_by_id(wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    wallet_repo.delete(wallet)
    return {"message": f"Wallet {wallet_id} deleted successfully"}
"""