# crypto_tracker/services/service_manager.py
from crypto_tracker.services.pair_service import PairService
from crypto_tracker.services.token_service import TokenService
from crypto_tracker.services.trade_service import TradeService
from crypto_tracker.services.mac_number_price_sync import MacNumbersPriceSyncService
from crypto_tracker.services.transaction_service import TransactionService
from crypto_tracker.services.wallet_service import WalletService


class ServiceManager:
    def __init__(self):
        self.mac_numbers_price_sync = MacNumbersPriceSyncService()
        self.wallet_service = WalletService()
        self.trade_service = TradeService()
        self.pair_service = PairService()
        self.token_service = TokenService()
        self.transaction_service = TransactionService()

