# crypto_tracker/services/wallet_service.py
from wireup import service

from crypto_tracker.database import Database
from crypto_tracker.configs.logger import Logger
from crypto_tracker.repositories.models.base import PairORM, TokenORM

@service
class PairService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()

    def add_pair(self, pair:PairORM) -> PairORM:
        base_token: TokenORM = self.db.token_repo.get_by_id(pair.base_token_id)
        quote_token: TokenORM = self.db.token_repo.get_by_id(pair.quote_token_id)
        pair.symbol = base_token.symbol + "/" + quote_token.symbol
        return self.db.pair_repo.create(pair)

    def add_pair_if_not_exists(self, pair:PairORM) -> PairORM:
        existing_pair = self.db.pair_repo.get_pair_by_address(pair.pair_address)
        if not existing_pair:
            self.logger.info(f'Pair {pair.symbol} does not exist creating it')
            return self.db.pair_repo.create(pair)
        return existing_pair

    def get_pairs(self) -> [PairORM]:
        return self.db.pair_repo.get_all()

    def get_pair(self, pair_id: int) -> PairORM:
        return self.db.pair_repo.get_by_id(pair_id)
