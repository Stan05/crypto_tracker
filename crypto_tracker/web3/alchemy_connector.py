from web3 import Web3
from ..config import Config

config = Config()

ALCHEMY_BASE_URL = config.ALCHEMY_BASE_URL
web3 = Web3(Web3.HTTPProvider(ALCHEMY_BASE_URL))

# Check connection
if web3.is_connected():
    print("Connected to Base network")
else:
    print("Failed to connect")
