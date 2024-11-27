# crypto_tracker/repositories_new/database.py
from .models import Base
from ..config import Config
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


