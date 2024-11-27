from typing import List
from ..logger import Logger
from ..models import Symbol
from crypto_tracker.service_manager import ServiceManager
from ..config import Config

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
    logger.info("Trades updated successfully!")
