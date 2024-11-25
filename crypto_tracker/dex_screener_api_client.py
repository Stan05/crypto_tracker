import requests
from sqlalchemy.dialects.postgresql.psycopg import logger

from .config import Config
from .logger import Logger

class DexScreenerApiClient:
    def __init__(self):
        self.config = Config()
        self.logger = Logger()

    def fetch_current_price(self, chain_id:str, pair_id:str):
        try:
            response = requests.get(
                f"https://api.dexscreener.com/latest/dex/pairs/{chain_id.lower()}/{pair_id}",
                headers={},
            )
            data = response.json()
            if data:
                return data['pairs'][0]['priceUsd']
            return None
        except Exception as e:
            self.logger.error(f"Error fetching ticker price for {symbol}: {e}")
            return None
            