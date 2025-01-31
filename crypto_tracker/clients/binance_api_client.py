from binance.spot import Spot
from wireup import service, Inject

from crypto_tracker.models import Trade, Symbol
from typing import List, Annotated
from datetime import datetime
from crypto_tracker.utils import to_datetime

@service
class BinanceAPIClient:
    def __init__(self, binance_spot_client: Annotated[Spot, Inject()]):
        self.client = binance_spot_client

    def fetch_trades(self, symbol:Symbol, last_updated_on:datetime) -> List[Trade]:
        try:

            trades = self.client.get_orders(
                symbol=symbol.to_plain_text()

            )

            # Convert the fetched trades into Trade objects
            trade_objects = [
                Trade(
                    order_id=trade['orderId'],
                    symbol=symbol,
                    price=float(trade['price']),
                    qty=float(trade['origQty']),
                    side=trade['side'],
                    status=trade['status'],
                    platform="Binance",
                    created_on=to_datetime(trade['time']),
                    updated_on=to_datetime(trade['updateTime'])
                )
                for trade in trades
            ]
            return trade_objects
        
        except Exception as e:
            print(f"Error fetching trades for {symbol}: {e}")
            return []
        
    def fetch_current_price(self, symbol:str):
        try:
            print(f'Fetching price for symbol {symbol}')
            tickers_price = self.client.ticker_price(symbol=symbol)
        
            if tickers_price:
                return tickers_price['price']
            return None
        except Exception as e:
            print(f"Error fetching ticker price for {symbol}: {e}")
            return None
            