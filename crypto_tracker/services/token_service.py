# crypto_tracker/services/token_service.py
from crypto_tracker.database import Database
from crypto_tracker.logger import Logger
from crypto_tracker.repositories.models.base import TradeORM, TokenORM


class TokenService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()

    def add_token(self, token:TokenORM) -> TokenORM:
        return self.db.token_repo.create(token)

    def add_token_if_not_exists(self, token:TokenORM) -> TokenORM:
        self.logger.info(f"Checking {token.name}, {token.symbol}, {token.address}")
        if not self.db.token_repo.exists(token.address):
            self.logger.info(f'Token {token.id} does not exist creating it')

            return self.db.token_repo.create(token)

        return token

    def get_tokens(self) -> [TokenORM]:
        return self.db.token_repo.get_all()

    def get_token(self, token_id: int) -> TokenORM:
        return self.db.token_repo.get_by_id(token_id)
