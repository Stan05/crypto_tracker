# crypto_tracker/services/token_service.py
from typing import Annotated

from wireup import service, Inject

from crypto_tracker.configs.logger import Logger
from crypto_tracker.repositories.models.base import TokenORM
from crypto_tracker.repositories.token_repository import TokenRepository


@service
class TokenService:
    def __init__(self,
                 token_repo: Annotated[TokenRepository, Inject()],
                 logger: Annotated[Logger, Inject()]):
        self.token_repo = token_repo
        self.logger = logger

    def add_token(self, token:TokenORM) -> TokenORM:
        return self.token_repo.create(token)

    def add_token_if_not_exists(self, token:TokenORM) -> TokenORM:
        existing_token = self.token_repo.get_token_by_address(token.address)
        if not existing_token:
            self.logger.info(f'Token {token.name} does not exist creating it')
            return self.token_repo.create(token)
        return existing_token

    def get_tokens(self) -> [TokenORM]:
        return self.token_repo.get_all()

    def get_token(self, token_id: int) -> TokenORM:
        return self.token_repo.get_by_id(token_id)
