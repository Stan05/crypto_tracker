from aiohttp.log import client_logger

from ..clients_manager import ClientsManager
from ..repositories.database import Database
from ..models import TradePair, PairPriceSnapshot, Symbol, Trade
from typing import List

class PnlCalculatorService:
    def __init__(self):
        self.db = Database()
        self.clients_manager = ClientsManager()
        self.client = self.clients_manager.binance_api

    def calculate(self):
        trade_pairs: List[TradePair] = self.db.trade_pair_repo.get_trade_pairs()
        price_snapshots: List[PairPriceSnapshot] = self.db.pair_price_snapshot_repo.get_price_snapshots()
        price_snapshots_dict: dict[Symbol, PairPriceSnapshot] = {price_snapshot.symbol: price_snapshot for price_snapshot in price_snapshots}
        
        print("Available pairs:")
        for trade_pair in trade_pairs:
            # Combine ticker_buy and ticker_sell to create the symbol
            symbol = Symbol(
                ticker_buy = trade_pair.ticker_buy, 
                ticker_sell = trade_pair.ticker_sell
            )

            price_snapshot = price_snapshots_dict[symbol]
            percentage_diff = ((price_snapshot.current_price - trade_pair.average_buy_price) / trade_pair.average_buy_price) * 100

            print(f"[{symbol.with_separator()}] - PnL: [{percentage_diff:.2f}%] average buy price: {trade_pair.average_buy_price}, current price: {price_snapshot.current_price} as of: {price_snapshot.updated_on}")

    def calculate_average_buy_price(self, trades: List[Trade]) -> float:
            # Initialize variables for average buy price calculation
            total_cost = 0.0
            total_quantity = 0.0

            # Loop through trades and filter only 'buy' trades
            for trade in trades:
                if trade.side.lower() == 'buy':
                    total_cost += trade.price * trade.qty  # Sum the total cost (price * quantity)
                    total_quantity += trade.qty  # Sum the total quantity
            

            # Calculate the average buy price
            if total_quantity > 0:
                return total_cost / total_quantity
            else:
                return None

    def __del__(self):
        # Ensure the database connection is closed when the TradeManager is destroyed
        self.db.close