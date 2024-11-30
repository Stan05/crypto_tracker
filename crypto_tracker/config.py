# Config consts
import configparser
import os

CFG_FL_NAME = "user.cfg"
USER_CFG_SECTION = "binance_user_config"

class Config: 
    def __init__(self):
        # Init config
        config = configparser.ConfigParser()
        config["DEFAULT"] = {
        }

        if not os.path.exists(CFG_FL_NAME):
            print("No configuration file (user.cfg) found! See README. Assuming default config...")
            config[USER_CFG_SECTION] = {}
        else:
            config.read(CFG_FL_NAME)

        # Get config for binance
        self.BINANCE_API_KEY = os.environ.get("API_KEY") or config.get(USER_CFG_SECTION, "api_key")
        self.BINANCE_API_SECRET_KEY = os.environ.get("API_SECRET_KEY") or config.get(USER_CFG_SECTION, "api_secret_key")
        self.BINANCE_TLD = os.environ.get("TLD") or config.get(USER_CFG_SECTION, "tld")

        # Get DB properties
        self.DB_URL = os.environ.get("DB_URI") or config.get(USER_CFG_SECTION, "DB_URI")

        supported_coin_list_values = os.environ.get("SUPPORTED_COIN_LIST") or config.get(USER_CFG_SECTION, "SUPPORTED_COIN_LIST")
        # Get supported coin list from the environment
        supported_coin_list = [
            coin.strip() for coin in supported_coin_list_values.split(',') if coin.strip()
        ]
        
        # Get supported coin list from supported_coin_list file
        if not supported_coin_list and os.path.exists("supported_coin_list"):
            with open("supported_coin_list") as rfh:
                for line in rfh:
                    line = line.strip()
                    if not line or line.startswith("#") or line in supported_coin_list:
                        continue
                    supported_coin_list.append(line)
        self.SUPPORTED_COIN_LIST = supported_coin_list

        # Alchemy
        self.ALCHEMY_BASE_URL = os.environ.get("ALCHEMY_BASE_URL") or config.get(USER_CFG_SECTION, "ALCHEMY_BASE_URL")