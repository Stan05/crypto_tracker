# crypto_tracker/services/token_service.py
from wireup import service

from crypto_tracker.database import Database
from crypto_tracker.configs.logger import Logger
from crypto_tracker.repositories.models.base import TokenORM

@service
class TokenService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()

    def add_token(self, token:TokenORM) -> TokenORM:
        return self.db.token_repo.create(token)

    def add_token_if_not_exists(self, token:TokenORM) -> TokenORM:
        existing_token = self.db.token_repo.get_token_by_address(token.address)
        if not existing_token:
            self.logger.info(f'Token {token.name} does not exist creating it')
            return self.db.token_repo.create(token)
        return existing_token

    def get_tokens(self) -> [TokenORM]:
        return self.db.token_repo.get_all()

    def get_token(self, token_id: int) -> TokenORM:
        return self.db.token_repo.get_by_id(token_id)
