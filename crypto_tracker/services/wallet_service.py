# crypto_tracker/services/wallet_service.py
from crypto_tracker.models_new import ChainIdType
from crypto_tracker.repositories_new.database import Database
from crypto_tracker.repositories_new.models.base import WalletORM


class WalletService:
    def __init__(self):
        self.db = Database()

    def add_wallet(self, wallet_address:str, chain_id:ChainIdType, name:str):
        wallet: WalletORM = WalletORM(address=wallet_address, chain_id=chain_id.name, name=name)
        self.db.wallet_repo.create(wallet)

