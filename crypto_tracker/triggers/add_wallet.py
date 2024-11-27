
from ..logger import Logger
from ..services.mac_number_price_sync import MacNumbersPriceSyncService

logger = Logger()

def add_wallet(address: str, chain_id: str):
    logger.info(f"Adding wallet with address: {address} and chain ID: {chain_id}")
    # Simulated logic for adding a wallet
    logger.info(f"Wallet {address} added successfully to chain {chain_id}!")
