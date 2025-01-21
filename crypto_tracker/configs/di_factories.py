import contextlib
from typing import Iterator

from binance.spot import Spot
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from wireup import service

from crypto_tracker.configs.settings import Settings

from crypto_tracker.repositories.models.base import Base


@service
def binance_spot_factory(settings: Settings) -> Spot:
    return Spot(api_key=settings.binance_api_key, api_secret=settings.binance_api_secret)

@service
def db_session_factory(settings: Settings) -> Iterator[Session]:
    db_engine = create_engine(settings.db_uri)
    with contextlib.closing(Session(bind=db_engine)) as db:
        Base.metadata.create_all(db_engine)
        yield db