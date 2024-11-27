
from ..logger import Logger
from ..services.service_manager import ServiceManager

logger = Logger()

def update_current_prices():
    logger.info("Updating Current Prices...")
    service_manager = ServiceManager()
    service_manager.price_service.fetch_and_store_current_prices()
