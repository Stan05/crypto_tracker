from crypto_tracker.clients.binance_api_client import BinanceAPIClient
from crypto_tracker.clients.dex_screener_api_client import DexScreenerApiClient


class ClientsManager:
    def __init__(self):
        self.dex_screener_api = DexScreenerApiClient()
        self.binance_api = BinanceAPIClient()