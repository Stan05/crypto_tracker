# crypto_tracker/services/wallet_service.py
from typing import Annotated

from wireup import service, Inject

from crypto_tracker.configs.logger import Logger
from crypto_tracker.repositories.models.base import PairORM, TokenORM
from crypto_tracker.repositories.pair_repository import PairRepository
from crypto_tracker.repositories.token_repository import TokenRepository


@service
class PairService:
    def __init__(self,
                 pair_repo: Annotated[PairRepository, Inject()],
                 token_repo: Annotated[TokenRepository, Inject()],
                 logger: Annotated[Logger, Inject()]):
        self.pair_repo = pair_repo
        self.token_repo = token_repo
        self.logger = logger

    def add_pair(self, pair:PairORM) -> PairORM:
        base_token: TokenORM = self.token_repo.get_by_id(pair.base_token_id)
        quote_token: TokenORM = self.token_repo.get_by_id(pair.quote_token_id)
        pair.symbol = base_token.symbol + "/" + quote_token.symbol
        return self.pair_repo.create(pair)

    def add_pair_if_not_exists(self, pair:PairORM) -> PairORM:
        existing_pair = self.pair_repo.get_pair_by_address(pair.pair_address)
        if not existing_pair:
            self.logger.info(f'Pair {pair.symbol} does not exist creating it')
            return self.pair_repo.create(pair)
        return existing_pair

    def get_pairs(self) -> [PairORM]:
        return self.pair_repo.get_all()

    def get_pair(self, pair_id: int) -> PairORM:
        return self.pair_repo.get_by_id(pair_id)
