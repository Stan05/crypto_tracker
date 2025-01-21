from binance.spot import Spot
from wireup import service

from crypto_tracker.configs.settings import Settings


@service
def binance_spot_factory(settings: Settings) -> Spot:
    return Spot(api_key=settings.binance_api_key, api_secret=settings.binance_api_secret)
