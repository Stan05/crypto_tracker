# crypto_tracker/repositories_new/database.py
from crypto_tracker.repositories_new.models.base import Base
from crypto_tracker.repositories_new.pair_repository import PairRepository
from crypto_tracker.repositories_new.price_snapshot_repository import PriceSnapshotRepository
from crypto_tracker.repositories_new.token_repository import TokenRepository
from crypto_tracker.repositories_new.trade_repository import TradeRepository
from crypto_tracker.repositories_new.wallet_repository import WalletRepository
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

    def close(self):
        self.wallet_repo.close()
        self.trade_repo.close()
        self.token_repo.close()
        self.pair_repo.close()
        self.price_snapshot_repo.close()