from typing import Annotated

from wireup import Inject

from crypto_tracker.configs.logger import Logger
from ..models import ChainIdType
from ..services.wallet_service import WalletService

logger = Logger()

def add_wallet(address: str, chain_id: str, name:str, wallet_service: Annotated[WalletService, Inject()]):
    logger.info(f"Adding wallet with address: {address} and chain ID: {chain_id}")
    wallet_service.add_wallet(address, ChainIdType.from_name(chain_id), name)
    logger.info(f"Wallet {address} added successfully to chain {chain_id}!")
