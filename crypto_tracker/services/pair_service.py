# crypto_tracker/services/wallet_service.py
from crypto_tracker.database import Database
from crypto_tracker.repositories.models.base import TradeORM, PairORM, TokenORM


class PairService:
    def __init__(self):
        self.db = Database()

    def add_pair(self, pair:PairORM) -> PairORM:
        base_token: TokenORM = self.db.token_repo.get_by_id(pair.base_token_id)
        quote_token: TokenORM = self.db.token_repo.get_by_id(pair.quote_token_id)
        pair.symbol = base_token.symbol + "/" + quote_token.symbol
        return self.db.pair_repo.create(pair)

    def get_pairs(self) -> [PairORM]:
        return self.db.pair_repo.get_all()

    def get_pair(self, pair_id: int) -> PairORM:
        return self.db.pair_repo.get_by_id(pair_id)
