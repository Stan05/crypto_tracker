from datetime import datetime

import requests
from bs4 import BeautifulSoup

from crypto_tracker.logger import Logger
from crypto_tracker.models import Transaction, Swap, Token


class BaseScraper:

    def __init__(self):
        self.logger = Logger()

    def get_transaction(self, txn_id) -> Transaction:
        html_content = self.__fetch_data(txn_id)

        soup = BeautifulSoup(html_content, 'html.parser')

        transaction_hash = soup.select_one("#spanTxHash").text.strip()

        status = soup.select_one(".badge.bg-success").text.strip()

        # Extract the timestamp
        timestamp_element = soup.select_one("#showUtcLocalDate")
        if timestamp_element:
            data_timestamp = timestamp_element.get("data-timestamp")  # Get the data-timestamp attribute
            if data_timestamp:
                # Convert the timestamp to a datetime object
                timestamp = datetime.fromtimestamp(int(data_timestamp))
            else:
                timestamp = None
        else:
            timestamp = None
        # Extract From Address
        origin = soup.select_one(".from-address-col a").get("href").strip().split("/address/")[1]
        # Extract Swap details
        swap_element = soup.select_one("#wrapperContent")
        self.logger.info(f"Swap element {swap_element}")
        if swap_element:
            swap_text = swap_element.get_text(strip=True, separator=" ")
            self.logger.info(f"Swap text {swap_text}")
            # Parse the swap details
            swap_parts = swap_text.split()
            try:
                base_token_amount = swap_parts[1]
                base_token_symbol = swap_parts[3]
                base_token_address = swap_element.select_one("a")["href"].split("/token/")[1]
                quote_token_amount = swap_parts[5]
                quote_token_symbol = swap_parts[6]
                quote_token_address = swap_element.select("a")[1]["href"].split("/token/")[1]
                acquiring_usd_value = swap_parts[8].strip("()").replace("$", "")
                dex = swap_parts[-1]
            except IndexError as e:
                self.logger.error(f"Error parsing swap text: {e}")
                base_token_amount = base_token_symbol = base_token_address = quote_token_amount = acquiring_usd_value = quote_token_symbol = dex = None
        else:
            base_token_amount = base_token_symbol = base_token_address = quote_token_amount = acquiring_usd_value = quote_token_symbol = dex = None
        # Create the result object
        payload = {
            "Transaction Hash": transaction_hash,
            "Status": status,
            "Timestamp": timestamp,
            "From Address": origin,
            "Swap Details": {
                "Base Token Amount": base_token_amount,
                "Base Token Symbol": base_token_symbol,
                "Base Token Address": base_token_address,
                "Quote Token Amount": quote_token_amount,
                "Acquiring USD Value": acquiring_usd_value,
                "Quote Token Symbol": quote_token_symbol,
                "Quote Token Address": quote_token_address,
                "DEX": dex,
            }
        }
        self.logger.info(payload)
        return Transaction(
            id=txn_id,
            swap=Swap(
                base_token_amount = base_token_amount,
                quote_token_amount = quote_token_amount,
                amount_USD = acquiring_usd_value,
                origin = origin,
                base_token = Token(
                    address = base_token_address,
                    name = None, # fetch from the graph
                    symbol = base_token_symbol,
                ),
                quote_token = Token(
                        address = quote_token_address,
                        name = None, # fetch from the graph
                        symbol = quote_token_symbol,
                    ),
                timestamp = timestamp,
                pool_id = None # can fetch this from the graph with base and quote tokens probably
            ),
            payload=payload
        )

    def __fetch_data(self, txn_id):
        url = f"https://basescan.org/tx/{txn_id}"  # Replace with the target URL
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0",
            "sec-ch-ua": '"Chromium";v="130", "Opera";v="115", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "upgrade-insecure-requests": "1",
        }
        cookies = {
            "ASP.NET_SessionId": "tfhvn2c2band2pzdprul2lyh",
            "__cflb": "0H28vtoAdHDLg8sTeQQMiRCFaG8m9KqQmqmpSv7HNi8",
            "_ga_TWEL8GRQ12": "GS1.1.1736874736.1.0.1736874736.0.0.0",
            "_ga": "GA1.1.1339248593.1736874736",
            "basescan_offset_datetime": "+2",
        }

        response = requests.get(url, headers=headers, cookies=cookies)

        if response.status_code == 200:
            html_content = response.text
        else:
            self.logger.error(f"Failed to retrieve content. Status code: {response.status_code}")
            raise Exception

        return html_content