from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, NUMERIC, UniqueConstraint, false
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class TokenORM(Base):
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

class WalletORM(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100), nullable=False)
    chain_id = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    __table_args__ = (
        UniqueConstraint("address", "chain_id", name="uq_address_chain_id"),
    )

class TradeORM(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    pair_id = Column(Integer, ForeignKey("pairs.id"), nullable=False)
    trade_type = Column(String(10), nullable=False)
    native_price = Column(NUMERIC, nullable=False)
    usd_price = Column(NUMERIC, nullable=False)
    quantity = Column(NUMERIC, nullable=False)
    trade_timestamp = Column(TIMESTAMP, nullable=False)
    wallet = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    txn_id = Column(Integer, ForeignKey("transactions.id"))
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

class PriceSnapshotORM(Base):
    __tablename__ = "price_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    pair_id = Column(Integer, ForeignKey("pairs.id"), nullable=False)
    native_price = Column(NUMERIC, nullable=False)
    usd_price = Column(NUMERIC, nullable=False)
    market_cap = Column(NUMERIC, nullable=False)
    fdv = Column(NUMERIC, nullable=False)
    snapshot_timestamp = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

class TransactionORM(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String(150), nullable=False, index=True, unique=True)
    payload = Column(JSONB, nullable=False)
    type = Column(String(100), nullable=False)
    status = Column(String(15), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())