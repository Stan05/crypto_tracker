from binance.spot import Spot

from crypto_tracker.configs.logger import Logger
from ..clients.binance_api_client import BinanceAPIClient
from ..clients.dex_screener_api_client import DexScreenerApiClient
from ..config import Config
from ..services.mac_number_price_sync import MacNumbersPriceSyncService

"""
TODO: Manually instantiating is a workaround here
"""
def mac_numbers_price_sync():
    logger: Logger = Logger()
    config: Config = Config()

    mac_numbers_price_sync_service: MacNumbersPriceSyncService = MacNumbersPriceSyncService(logger,
                                                                                            DexScreenerApiClient(logger),
                                                                                            BinanceAPIClient(Spot(api_key=config.BINANCE_API_KEY, api_secret=config.BINANCE_API_SECRET_KEY)))
    logger.info("Updating Mac Numbers Prices...")
    mac_numbers_price_sync_service.update_altcoins_file()
    mac_numbers_price_sync_service.update_memecoins_file()
