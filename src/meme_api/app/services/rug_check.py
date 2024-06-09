import requests
import certifi
from meme_api.custom_logger import logger
import logging
from meme_api.configs import RUG_CHECK_USER_AGENT

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
        self.holders = 0

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "X-Wallet-Address": "null",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": RUG_CHECK_USER_AGENT,
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
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Rug Check Request Error {mint_address}: {e}")

    def calculate_pct(self, amount, total_supply, decimals):
        try:
            full_amount = amount / (10**decimals)
            pct = (full_amount / (total_supply / (10**decimals))) * 100
            return float(pct)
        except ZeroDivisionError:
            return 0

    async def check(self, mint_address, configs, coin_name):

        try:
            response = self.get_rug_check(mint_address)
        except Exception as e:
            self.pass_checks = False
            logger.error(f"{coin_name} : {e}")
            return

        try:
            # Check Holders
            holders = response.get("topHolders", [])
            nr_holders = len(holders)
            self.holders = holders

            # Nr of HOLD should not be 0 or greater than max
            if 0 < nr_holders > configs.current_holders:
                self.pass_checks = False
                logger.info(
                    f"RUGCHECK NOT PASSED {coin_name}: HOLDERS - Nr.holders {nr_holders} > {configs.current_holders} MAX.holders | {mint_address}"
                )
                return False

            # twitter_ipfs = response.get("tokenMeta", {}).get("uri", None)
            # if twitter_ipfs is not None:
            #     twitter_data = self.get_ipfs_data(twitter_ipfs)
            #     twitter = twitter_data.get('twitter', None)
            #     if twitter is None:
            #         self.pass_checks = False

            dev_holder = holders[1] if nr_holders > 2 else holders[0]
            dev_holder_pct = dev_holder.get("pct", None)
            if dev_holder_pct is None:
                dev_holder_pct = self.calculate_pct(
                    holder_amount=dev_holder.get("amount", 0),
                    total_supply=response.get("token", {}).get("supply", 1),
                    decimals=response.get("token", {}).get("decimals", 0),
                )

            if not (
                configs.dev_percentage_min
                <= dev_holder_pct
                <= configs.dev_percentage_max
            ):
                self.pass_checks = False
                logger.info(
                    f"RUGCHECK NOT PASSED {coin_name}: DEV PERCENTAGE {dev_holder_pct}% | {mint_address}"
                )
                return False

            logger.info(
                f"CHECKS PASSED {coin_name}: Nr HOLDR: {nr_holders}, DEV%: {dev_holder} | {mint_address}"
            )
            return self.pass_checks

        except Exception as e:
            logger.error(f"Rug Check Error for {coin_name}: {e}")
            return False
