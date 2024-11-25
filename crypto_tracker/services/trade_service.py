from ..binance_api_client import BinanceAPIClient
from ..repositories.database import Database
from ..models import Trade, Symbol, TradePair
from .pnl_calculator_service import PnlCalculatorService
from typing import List
from ..utils import is_within_X_minutes
from datetime import datetime

class TradeService:
    def __init__(self):
        self.api_client = BinanceAPIClient()
        self.db = Database()
        self.pnl_calculator_service = PnlCalculatorService()

    def fetch_and_store_trades(self, symbol:Symbol):

        last_updated_on = self.db.trade_pair_repo.get_last_trades_updated_on(symbol)
        
        if (last_updated_on and is_within_X_minutes(last_updated_on, 10)):
            print(f'Trades for {symbol} has been updated in the last 10 minutes, skipping')
            return

        trades: List[Trade] = self.api_client.fetch_trades(symbol, last_updated_on)

        for trade in trades:
            print(f'Upserting trade for {symbol}, side: {trade.side}, status: {trade.status}, price: {trade.price}, quantity: {trade.qty}')
            self.db.trade_repo.upsert_trade(trade)

    def update_trade_pair(self, symbol: Symbol):

        last_updated_on = self.db.trade_pair_repo.get_last_trades_updated_on(symbol)
        
        if (last_updated_on and is_within_X_minutes(last_updated_on, 10)):
            print(f'Pair for {symbol} has been updated in the last 10 minutes, skipping')
            return
        
        trades: List[Trade] = self.db.trade_repo.get_trades(symbol, "FILLED")
        print(f'Number of Filled Trades {len(trades)}')

        if not trades:
            print(f'Not available trades for {symbol.with_separator()}')
            return
        
        min_created_on = None
        max_updated_on = None
        available_quantity = 0.0

        # Loop through trades and filter only 'buy' trades
        for trade in trades:
            if trade.side.lower() == 'buy':
                available_quantity += trade.qty
            if trade.side.lower() == 'sell':
                available_quantity -= trade.qty    
            if not min_created_on or min_created_on > trade.created_on:
                min_created_on = trade.created_on
            if not max_updated_on or max_updated_on < trade.updated_on:
                max_updated_on = trade.updated_on

        average_buy_price = self.pnl_calculator_service.calculate_average_buy_price(trades)       
        print(f'Average buy price: {average_buy_price}, available quantity: {available_quantity}')

        self.db.trade_pair_repo.upsert_trade_pair(
            TradePair(
                ticker_buy=trade.symbol.split("/")[0],  
                ticker_sell=trade.symbol.split("/")[1], 
                average_buy_price=average_buy_price,
                available_quantity=available_quantity,
                first_trade_created_on=trade.created_on,
                last_trade_updated_on=trade.updated_on,
                trades_updated_on=datetime.now()
            )
        )

    def __del__(self):
        # Ensure the database connection is closed when the TradeManager is destroyed
        self.db.close