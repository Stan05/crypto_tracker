import subprocess
import time
from dataclasses import dataclass

from ..clients_manager import ClientsManager
from ..logger import Logger

@dataclass
class CoinMetadata:
    coin: str
    chain: str
    pair_address: str

    def is_complete(self) -> bool:
        """
        Checks if all fields are populated and do not contain 'None'.
        Returns:
            bool: True if all fields are populated and not 'None', False otherwise.
        """
        return all(
            getattr(self, field) != "None" and bool(getattr(self, field))
            for field in self.__dataclass_fields__
        )

class MacNumbersPriceSyncService:
    def __init__(self):
        self.clients_manager = ClientsManager()
        self.logger = Logger()

    def update_memecoins_file(self):
        coin_metadata_list:[CoinMetadata] = self.fetch_symbols_from_memecoins()

        for coin_metadata in coin_metadata_list:
            if coin_metadata.is_complete():
                self.logger.info(f"Fetching prices for {coin_metadata}")
                current_price = self.clients_manager.dex_screener_api.fetch_by_chain_and_pair_id(coin_metadata.chain, coin_metadata.pair_address)
                if not current_price:
                    pairs = self.clients_manager.dex_screener_api.fetch_by_token_address(coin_metadata.pair_address)
                    if pairs:
                        for pair in pairs:
                            if pair['chainId'] == coin_metadata.chain:
                                current_price = pair['priceUsd']
                                break

                if not current_price:
                    self.logger.warning(f"Could not fetch current price for {coin_metadata.coin}")
                    continue

                self.logger.info(f'Current price {current_price}')

                # AppleScript to update the Current Price column
                apple_script = f'''
                                tell application "Numbers"
                                    tell document "Crypto"
                                        tell sheet "Memecoins"
                                            tell table "Metadata"
                                                set rowCount to count of rows
                                                repeat with i from 2 to rowCount -- Start from row 2 to skip header
                                                    if value of cell i of column "A" is "{coin_metadata.coin}" then
                                                        set value of cell i of column "D" to "{str(current_price).replace('.', ',')}" -- Update column D
                                                        exit repeat
                                                    end if
                                                end repeat
                                            end tell
                                        end tell
                                    end tell
                                end tell
                            '''
                result = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
                if result.stderr:
                    self.logger.error(f"Error updating price for {coin_metadata.coin}: {result.stderr.encode('utf-8')}")
                else:
                    self.logger.info(f"Successfully updated price for {coin_metadata.coin}")
            time.sleep(1)  # Adjust the delay as needed

    def update_altcoins_file(self):
        self.logger.info('Fetching symbols from Numbers...')
        symbols = self.fetch_symbols_from_altcoins()
        if not symbols:
            self.logger.info("No symbols found in column A.")
            return

        self.logger.info(f"Found symbols: {symbols}")

        # Loop through symbols, fetch prices, and update the table
        for index, symbol in enumerate(symbols, start=2):
            try:
                # Fetch price from API
                self.logger.info(f"Fetching price for {symbol}...")
                current_price = self.clients_manager.binance_api.fetch_current_price(symbol=f'{symbol}USDT')
                self.logger.info(f"Fetched price for {symbol}: {current_price}")

                # Update price in corresponding row in column F
                apple_script = f'''
                     tell application "Numbers"
                         tell document "Crypto"
                             tell sheet "Altcoins"
                                 tell table "Altcoins"
                                     set value of cell {index} of column "F" to "{str(current_price).replace('.', ',')}"
                                 end tell
                             end tell
                         end tell
                     end tell
                 '''
                result = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
                if result.stderr:
                    self.logger.error(f"Error updating price for {symbol}: {result.stderr}")
                else:
                    self.logger.info(f"Updated price for {symbol} in row {index}.")
            except Exception as e:
                self.logger.error(f"Error fetching/updating price for {symbol}: {e}")

            # Delay between API calls
            time.sleep(1)  # Adjust the delay as needed

    def fetch_symbols_from_altcoins(self):
        # AppleScript to read symbols from column A
        apple_script = '''
            tell application "Numbers"
                tell document "Crypto"
                    tell sheet "Altcoins"
                        tell table "Altcoins"
                            set symbols to value of cells of column "A"
                        end tell
                    end tell
                end tell
            end tell
            return items 2 thru -1 of symbols -- Skip the first row (header)
        '''
        result = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
        if result.stderr:
            self.logger.error("Error reading symbols:", result.stderr)
            return []
        symbols = result.stdout.strip().split(", ")
        return [symbol.strip() for symbol in symbols if symbol.strip()]

    def fetch_symbols_from_memecoins(self):
        # AppleScript to read values from columns A, B, and C
        apple_script = '''
                tell application "Numbers"
                    tell document "Crypto"
                        tell sheet "Memecoins"
                            tell table "Metadata"
                                set rowCount to count of rows
                                set metadata to {}
                                repeat with i from 2 to rowCount -- Start from row 4
                                    set coinValue to value of cell i of column "A"
                                    set chainValue to value of cell i of column "B"
                                    set pairValue to value of cell i of column "C"
                                    if coinValue is missing value then
                                        set coinValue to "None"
                                    end if
                                    if chainValue is missing value then
                                        set chainValue to "None"
                                    end if
                                    if pairValue is missing value then
                                        set pairValue to "None"
                                    end if
                                    set end of metadata to coinValue & "|" & chainValue & "|" & pairValue & ","
                                end repeat
                            end tell
                        end tell
                    end tell
                end tell
                return metadata as text
            '''
        result = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)

        # Check for errors
        if result.stderr:
            self.logger.error(f"Error reading metadata: {result.stderr.decode('utf-8')}")
            return []

        # Parse the AppleScript output
        try:
            raw_output = result.stdout.strip()
            self.logger.info(f"Raw AppleScript output: {raw_output}")
            rows = raw_output.split(",")  # Split rows by ', '
            metadata = [
                CoinMetadata(*row.split("|")) for row in rows if len(row.split("|")) == 3
            ]
            return metadata
        except Exception as e:
            self.logger.error(f"Error parsing AppleScript output: {e}")
            return []

