import requests
from sqlalchemy.dialects.postgresql.psycopg import logger

from crypto_tracker.config import Config
from crypto_tracker.logger import Logger

class DexScreenerApiClient:
    def __init__(self):
        self.config = Config()
        self.logger = Logger()

    def fetch_by_chain_and_pair_id(self, chain_id:str, pair_id:str):
        try:
            response = requests.get(
                f"https://api.dexscreener.com/latest/dex/pairs/{chain_id.lower()}/{pair_id}",
                headers={},
            )
            data = response.json()
            if data and data['pairs']:
                return data['pairs'][0]['priceUsd']
            return None
        except Exception as e:
            self.logger.error(f"Error fetching ticker price for {chain_id}/{pair_id}: {e}")
            return None

    def fetch_by_token_address(self, token_addr: str):
        try:
            response = requests.get(
                f"https://api.dexscreener.com/latest/dex/tokens/{token_addr}",
                headers={},
            )
            data = response.json()
            if data and data['pairs']:
                return data['pairs']
            return None
        except Exception as e:
            self.logger.error(f"Error fetching ticker price for {symbol}: {e}")
            return None
