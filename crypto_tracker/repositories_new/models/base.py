from sqlalchemy import Column, Integer, BigInteger, Float, String, DateTime, TIMESTAMP, ForeignKey, false
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class TokenOrm(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    symbol = Column(String(50), nullable=False, unique=True)
    address = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now())

class PairORM(Base):
    __tablename__ = "pairs"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False, unique=True)
    base_token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    quote_token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    chain_id = Column(String(50), nullable=False)
    dex_id = Column(String(50), nullable=False)
    pair_address = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
