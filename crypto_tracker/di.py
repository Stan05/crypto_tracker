import wireup
from binance.spot import Spot
from wireup import service

from crypto_tracker import services, configs, clients

container = wireup.create_container(
    # Parameters serve as application/service configuration.
    # Let the container know where service registrations are located.
    service_modules=[services, configs, clients]
)
"""
container = wireup.create_container(
    # Parameters serve as application/service configuration.
    # Let the container know where service registrations are located.
    service_modules=[services]
)


parameters={
    "redis_url": os.environ["APP_REDIS_URL"],
    "weather_api_key": os.environ["APP_WEATHER_API_KEY"],
},
"""