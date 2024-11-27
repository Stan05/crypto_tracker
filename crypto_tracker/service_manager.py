# crypto_tracker/services/service_manager.py

from crypto_tracker.services.price_service import PriceService
from crypto_tracker.services.trade_service import TradeService
from crypto_tracker.services.pnl_calculator_service import PnlCalculatorService
from crypto_tracker.services.mac_number_price_sync import MacNumbersPriceSyncService
from crypto_tracker.services.wallet_service import WalletService


class ServiceManager:
    def __init__(self):
        self.price_service = PriceService()
        self.trade_service = TradeService()
        self.pnl_calculator_service = PnlCalculatorService()
        """New Services"""
        self.mac_numbers_price_sync = MacNumbersPriceSyncService()
        self.wallet_service = WalletService()

