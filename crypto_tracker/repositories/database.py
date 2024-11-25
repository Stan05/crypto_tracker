# crypto_tracker/database.py

from .trade_repository import TradeRepository
from .trade_pair_repository import TradePairRepository
from .pair_price_snapshot_repository import PairPriceSnapshotRepository
from ..config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base

# Initialize SQLAlchemy engine and session
config = Config()
engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine)

class Database:
    def __init__(self):
        # Create tables if they don't exist
        Base.metadata.create_all(engine)  # This ensures that all tables are created at startup

        self.session = Session()
        self.trade_repo = TradeRepository(self.session)
        self.trade_pair_repo = TradePairRepository(self.session)
        self.pair_price_snapshot_repo = PairPriceSnapshotRepository(self.session)

    def close(self):
        self.trade_repo.close()
        self.trade_pair_repo.close()
