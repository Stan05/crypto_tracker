from fastapi import APIRouter
from pydantic import BaseModel

from ..logger import Logger
from ..models_new import ChainIdType
from crypto_tracker.service_manager import ServiceManager

logger = Logger()
router = APIRouter()
service_manager = ServiceManager()

class WalletRequest(BaseModel):
    address: str
    chain_id: str
    name: str


class WalletResponse(BaseModel):
    id: int
    address: str
    chain_id: str


@router.post("/wallets", response_model=WalletResponse)
def add_wallet(request: WalletRequest):
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
    new_wallet = service_manager.wallet_service.add_wallet(wallet_address=request.address, chain_id=ChainIdType.from_name(request.chain_id), name=request.name)
    logger.info(f"Wallet successfully added")
    return WalletResponse(id=new_wallet.id, address=new_wallet.address, chain_id=new_wallet.chain_id)

"""
@router.get("/wallets", response_model=list[WalletResponse])
def get_wallets(db: Session = Depends(get_db)):
    \"""
    Retrieve all wallets.
    \"""
    wallet_repo = WalletRepository(db)
    wallets = wallet_repo.get_all()
    return [WalletResponse(id=w.id, address=w.address, chain_id=w.chain_id) for w in wallets]


@router.get("/wallets/{wallet_id}", response_model=WalletResponse)
def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
    \"""
    Retrieve a single wallet by ID.
    \"""
    wallet_repo = WalletRepository(db)
    wallet = wallet_repo.get_by_id(wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletResponse(id=wallet.id, address=wallet.address, chain_id=wallet.chain_id)


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