# crypto_tracker/apis/__init__.py

__version__ = "0.1.0"

from fastapi import APIRouter
from .wallet_api import router as wallets_router
from .trades_api import router as trades_router
from .pair_api import router as pairs_router

# Central API router
api_router = APIRouter()

# Include individual routers
api_router.include_router(wallets_router, prefix="/wallets", tags=["Wallets"])
api_router.include_router(trades_router, prefix="/trades", tags=["Trades"])
api_router.include_router(pairs_router, prefix="/pairs", tags=["Pairs"])