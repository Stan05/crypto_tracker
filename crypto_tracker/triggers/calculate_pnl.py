
from ..logger import Logger
from crypto_tracker.service_manager import ServiceManager

logger = Logger()

def calculate_pnl():
    logger.info("Calculating PnL...")
    service_manager = ServiceManager()
    service_manager.pnl_calculator_service.calculate()
