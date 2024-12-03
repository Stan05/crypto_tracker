# crypto_tracker/repositories/database.py
from crypto_tracker.repositories.models.base import Base
from crypto_tracker.repositories.pair_repository import PairRepository
from crypto_tracker.repositories.price_snapshot_repository import PriceSnapshotRepository
from crypto_tracker.repositories.token_repository import TokenRepository
from crypto_tracker.repositories.trade_repository import TradeRepository
from crypto_tracker.repositories.transaction_repository import TransactionRepository
from crypto_tracker.repositories.wallet_repository import WalletRepository
from crypto_tracker.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Initialize SQLAlchemy engine and session
config = Config()
engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine)

class Database:
    def __init__(self):
        # Create tables if they don't exist
        Base.metadata.create_all(engine)  # This ensures that all tables are created at startup

        self.session = Session()
        self.wallet_repo = WalletRepository(self.session)
        self.trade_repo = TradeRepository(self.session)
        self.token_repo = TokenRepository(self.session)
        self.pair_repo = PairRepository(self.session)
        self.price_snapshot_repo = PriceSnapshotRepository(self.session)
        self.transaction_repo = TransactionRepository(self.session)

    def close(self):
        self.wallet_repo.close()
        self.trade_repo.close()
        self.token_repo.close()
        self.pair_repo.close()
        self.price_snapshot_repo.close()