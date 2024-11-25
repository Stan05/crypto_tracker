from ..binance_api_client import BinanceAPIClient
from ..repositories.database import Database
from ..models import Symbol, PairPriceSnapshot
from typing import List
from datetime import datetime, timedelta
from ..utils import is_within_X_minutes

class PriceService:
    def __init__(self):
        self.api_client = BinanceAPIClient()
        self.db = Database()

    def fetch_and_store_current_prices(self):
        symbols: List[Symbol] = self.db.trade_pair_repo.get_unique_symbols()
        for symbol in symbols:

            last_updated_on = self.db.pair_price_snapshot_repo.get_last_updated_on(symbol)
            
            if (last_updated_on and is_within_X_minutes(last_updated_on, 10)):
                print(f'Price has been updated for {symbol} in the last 10 minutes, skipping.')
                continue
            
            print(f'Updating current price for {symbol.to_plain_text()}')
            
            ticker_current_price = self.api_client.fetch_current_price(symbol.to_plain_text())
            print(f'Current price {ticker_current_price}')
            
            self.db.pair_price_snapshot_repo.upsert_price_snapshot(PairPriceSnapshot(
                symbol=symbol,
                current_price=ticker_current_price,
                created_on=datetime.now(),
                updated_on=datetime.now()
            ))

    def __del__(self):
        # Ensure the database connection is closed when the TradeManager is destroyed
        self.db.close