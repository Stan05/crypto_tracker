
from ..logger import Logger
from ..models_new import ChainIdType
from crypto_tracker.service_manager import ServiceManager

logger = Logger()

def add_wallet(address: str, chain_id: str, name:str):
    logger.info(f"Adding wallet with address: {address} and chain ID: {chain_id}")
    service_manager = ServiceManager()
    service_manager.wallet_service.add_wallet(address, ChainIdType.from_name(chain_id), name)
    logger.info(f"Wallet {address} added successfully to chain {chain_id}!")
