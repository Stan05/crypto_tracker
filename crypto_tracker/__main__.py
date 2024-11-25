# crypto_tracker/__main__.py
from sqlalchemy.dialects.postgresql.psycopg import logger

from .services.service_manager import ServiceManager
from .services.mac_number_price_sync import MacNumbersPriceSyncService
from .models import Symbol
from .config import Config
from typing import List
import argparse
from .logger import Logger

logger = Logger()

def update_trades():

    logger.info("Updating trades...")
    service_manager = ServiceManager()
    config = Config()



    # Fetch and store trades for your trading pairs
    trading_symbols: List[Symbol] = []

    for ticker in config.SUPPORTED_COIN_LIST:
        ticker_buy, ticker_sell = ticker.split('/')
        trading_symbols.append(Symbol(ticker_buy, ticker_sell))

    for symbol in trading_symbols:
        logger.info(f'Updating trades for {symbol}')
        service_manager.trade_service.fetch_and_store_trades(symbol)

        logger.info(f'Updating pair for {symbol}')
        service_manager.trade_service.update_trade_pair(symbol)

def calculate_pnl():
    logger.info("Calculating PnL...")
    service_manager = ServiceManager()
    service_manager.pnl_calculator_service.calculate()

def update_current_prices():
    logger.info("Updating Current Prices...")
    service_manager = ServiceManager()
    service_manager.price_service.fetch_and_store_current_prices()
    
def mac_numbers_price_sync():
    logger.info("Updating Mac Numbers Prices...")
    mac_numbers_price_sync_service = MacNumbersPriceSyncService()
    mac_numbers_price_sync_service.update_altcoins_file()
    mac_numbers_price_sync_service.update_memecoins_file()

def test():
    api = MacNumbersPriceSyncService()
    api.update_memecoins_file()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Crypto Tracker Utility')
    
    # Add entry points
    parser.add_argument(
        'command', 
        choices=['update_trades', 'calculate_pnl', 'update_current_prices', 'mac_numbers_price_sync', 'test'],
        help='Specify which operation to perform: update_trades or calculate_pnl'
    )

    # Parse arguments
    args = parser.parse_args()

    # Run based on the argument passed
    if args.command == 'update_trades':
        update_trades()
    elif args.command == 'calculate_pnl':
        calculate_pnl()
    elif args.command == 'update_current_prices':
        update_current_prices()
    elif args.command == 'mac_numbers_price_sync':
        mac_numbers_price_sync()
    elif args.command == 'test':
        test()