
from crypto_tracker.configs.logger import Logger
from ..services.mac_number_price_sync import MacNumbersPriceSyncService

logger = Logger()

def mac_numbers_price_sync():
    logger.info("Updating Mac Numbers Prices...")
    mac_numbers_price_sync_service = MacNumbersPriceSyncService()
    mac_numbers_price_sync_service.update_altcoins_file()
    mac_numbers_price_sync_service.update_memecoins_file()
