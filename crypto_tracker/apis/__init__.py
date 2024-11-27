# crypto_tracker/apis/__init__.py

__version__ = "0.1.0"

from fastapi import APIRouter
from .wallet_api import router as wallets_router

# Central API router
api_router = APIRouter()

# Include individual routers
api_router.include_router(wallets_router, prefix="/wallets", tags=["Wallets"])