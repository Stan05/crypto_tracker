# crypto_tracker/services/service_manager.py

from .price_service import PriceService
from .trade_service import TradeService
from .pnl_calculator_service import PnlCalculatorService
from .mac_number_price_sync import MacNumbersPriceSyncService
from .wallet_service import WalletService


class ServiceManager:
    def __init__(self):
        self.price_service = PriceService()
        self.trade_service = TradeService()
        self.pnl_calculator_service = PnlCalculatorService()
        """New Services"""
        self.mac_numbers_price_sync = MacNumbersPriceSyncService()
        self.wallet_service = WalletService()

