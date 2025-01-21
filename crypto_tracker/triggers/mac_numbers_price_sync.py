
from crypto_tracker.configs.logger import Logger
from ..clients.binance_api_client import BinanceAPIClient
from ..clients.dex_screener_api_client import DexScreenerApiClient
from ..services.mac_number_price_sync import MacNumbersPriceSyncService

"""
TODO: Manually instantiating is a workaround here
"""
def mac_numbers_price_sync():
    logger: Logger = Logger()
    mac_numbers_price_sync_service: MacNumbersPriceSyncService = MacNumbersPriceSyncService(logger,
                                                                                            DexScreenerApiClient(logger),
                                                                                            BinanceAPIClient())
    logger.info("Updating Mac Numbers Prices...")
    mac_numbers_price_sync_service.update_altcoins_file()
    mac_numbers_price_sync_service.update_memecoins_file()
