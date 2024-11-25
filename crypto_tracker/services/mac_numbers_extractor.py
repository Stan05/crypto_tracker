import subprocess
from ..logger import Logger
from .mac_number_price_sync import CoinMetadata


class MacNumbersExtractor:
    def __init__(self):
        self.logger = Logger()

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
            self.logger.error(f"Error reading symbols: {result.stderr}")
            return []
        symbols = result.stdout.strip().split(", ")
        return [symbol.strip() for symbol in symbols if symbol.strip()]

    def update_altcoin_price(self, symbol:str, column_index:int, current_price:str):
        # Update price in corresponding row in column F
        apple_script = f'''
             tell application "Numbers"
                 tell document "Crypto"
                     tell sheet "Altcoins"
                         tell table "Altcoins"
                             set value of cell {column_index} of column "F" to "{str(current_price).replace('.', ',')}"
                         end tell
                     end tell
                 end tell
             end tell
         '''
        result = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
        if result.stderr:
            self.logger.error(f"Error updating price for {symbol}: {result.stderr}")
        else:
            self.logger.info(f"Updated price for {symbol} in row {column_index}.")

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

    def update_memecoin_price(self, coin:str, current_price:str):

        # AppleScript to update the Current Price column
        apple_script = f'''
                        tell application "Numbers"
                            tell document "Crypto"
                                tell sheet "Memecoins"
                                    tell table "Metadata"
                                        set rowCount to count of rows
                                        repeat with i from 2 to rowCount -- Start from row 2 to skip header
                                            if value of cell i of column "A" is "{coin}" then
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
            self.logger.error(f"Error updating price for {coin}: {result.stderr.encode('utf-8')}")
        else:
            self.logger.info(f"Successfully updated price for {coin}")