# crypto_tracker/services/token_service.py
from crypto_tracker.database import Database
from crypto_tracker.repositories_new.models.base import TradeORM, TokenORM


class TokenService:
    def __init__(self):
        self.db = Database()

    def add_token(self, token:TokenORM) -> TokenORM:
        return self.db.token_repo.create(token)

    def get_tokens(self) -> [TokenORM]:
        return self.db.token_repo.get_all()

    def get_token(self, token_id: int) -> TokenORM:
        return self.db.token_repo.get_by_id(token_id)
