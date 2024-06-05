import requests
import certifi
from meme_api.custom_logger import logger
import logging

logger_2 = logging.getLogger(__name__)
logger_2.setLevel(logging.INFO)

file_handler = logging.FileHandler("risks.log", mode="w")
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger_2.addHandler(file_handler)

class RugCheck:
    """Scrape info for coins"""

    def __init__(self):
        self.pass_checks = True

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "X-Wallet-Address": "null",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"macOS"',
        "Accept": "/",
        "Origin": "https://rugcheck.xyz",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://rugcheck.xyz/",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
    ca_bundle_path = certifi.where()
    url = "https://api.rugcheck.xyz/v1/tokens"

    def get_ipfs_data(self, ipfs_uri):
        try:
            response = requests.get(ipfs_uri)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger_2.error(f"IPFS Request Error: {e}")
            return None

    def get_rug_check(self, mint_address):
        try:
            response = requests.get(
                url=f"{self.url}/{mint_address}/report",
                headers=self.headers,
                verify=self.ca_bundle_path,
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Rug Check Request Error for {mint_address}: {e}")
            return None

    def calculate_pct(self, amount, total_supply, decimals):
        try:
            full_amount = amount / (10 ** decimals)
            pct = (full_amount / (total_supply / (10 ** decimals))) * 100
            return pct
        except ZeroDivisionError:
            return 0

    async def check(self, mint_address, config, coin_name):
        self.pass_checks = True
        response = self.get_rug_check(mint_address)

        if response is None:
            logger.info(f"RUG CHECK failed for {mint_address}. Response is None.")
            self.pass_checks = False
            return

        try:
            if response.status_code != 200:
                logger.info(f"RUG CHECK Error status code: {response.status_code} for {coin_name}")
                self.pass_checks = False
                return

            _response = response.json()

            logger.info(f"PASS CHECK 1 {self.pass_checks}")

            # Check Holders
            holders = _response.get("topHolders", [])
            nr_holders = len(holders)
            self.holders = holders

            total_supply = _response.get("token", {}).get("supply", 1)
            decimals = _response.get("token", {}).get("decimals", 0)
            twitter_ipfs = _response.get("tokenMeta", {}).get("uri", None)

            if twitter_ipfs is not None:
                twitter_data = self.get_ipfs_data(twitter_ipfs)
                twitter = twitter_data.get('twitter', None)
                if twitter is None:
                    self.pass_checks = False

            if len(holders) > 1:
                holder_pct = holders[1].get('pct', None)
                if holder_pct is None:
                    holder_amount = holders[1].get('amount', 0)
                    holder_pct = self.calculate_pct(holder_amount, total_supply, decimals)
                dev_holder = float(holder_pct)
            elif len(holders) > 0:
                holder_pct = holders[0].get('pct', None)
                if holder_pct is None:
                    holder_amount = holders[0].get('amount', 0)
                    holder_pct = self.calculate_pct(holder_amount, total_supply, decimals)
                dev_holder = float(holder_pct)
            else:
                logger.info(f"Holders are {holders}")
                dev_holder = float(110)
                logger.warning(f"No holders found, defaulting dev holder to 110.")

            logger.info(f"Number of holders: {nr_holders}, Dev holder percentage: {dev_holder} for {coin_name}")

            if nr_holders > config.current_holders:
                self.pass_checks = False
                logger.info(f"RUG CHECK NOT PASSED {coin_name}: {nr_holders} > {config.current_holders}")
                logger.info(f"PASS CHECK 3 {self.pass_checks}")

            if not (config.dev_percentage_min <= dev_holder <= config.dev_percentage_max):
                self.pass_checks = False
                logger.info(f"RUG CHECK NOT PASSED PERCENTAGE {coin_name}: {dev_holder}")
                logger.info(f"PASS CHECK 4 {self.pass_checks}")

            logger.info(f"PASS CHECK 5 {self.pass_checks}")

        except Exception as e:
            logger.error(f"Rug Check Error for {coin_name}: {e}")

