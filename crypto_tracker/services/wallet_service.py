# crypto_tracker/services/wallet_service.py
from typing import Annotated

from wireup import service, Inject

from crypto_tracker.models import ChainIdType
from crypto_tracker.repositories.models.base import WalletORM
from crypto_tracker.repositories.wallet_repository import WalletRepository


@service
class WalletService:
    def __init__(self,
                 wallet_repo: Annotated[WalletRepository, Inject()],):
        self.wallet_repo = wallet_repo

    def add_wallet(self, wallet_address:str, chain_id:ChainIdType, name:str) -> WalletORM:
        wallet: WalletORM = WalletORM(address=wallet_address, chain_id=chain_id.name, name=name)
        return self.wallet_repo.create(wallet)

    def get_wallets(self) -> [WalletORM]:
        return self.wallet_repo.get_all()

    def get_wallet(self, wallet_id: int) -> WalletORM:
        return self.wallet_repo.get_by_id(wallet_id)
