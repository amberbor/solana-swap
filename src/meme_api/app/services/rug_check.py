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

    def get_rug_check(self, mint_address):
        return requests.get(
            url=f"{self.url}/{mint_address}/report",
            headers=self.headers,
            verify=self.ca_bundle_path,
        )

    async def check(self, mint_address, max_holders, coin_name):

        response = self.get_rug_check(mint_address)

        try:
            if response.status_code != 200:
                self.pass_checks = False
            _response = response.json()

            #Check Holders
            holders = _response.get("topHolders", [])
            nr_holders = len(holders)
            self.holders = holders
            if nr_holders >= max_holders:
                self.pass_checks = False
                logger.info(f"NOT PASSED {coin_name}: {nr_holders} >= {max_holders}")

            #Check Risks
            risks = _response.get("risks", [])
            self.risk_danger = False
            self.risk_warn = False
            for risk in risks:
                level = risk.get("level")
                name = risk.get('name')
                value = risk.get('value')
                if name == 'Single holder ownership':
                    self.pass_checks = False
                    self.risk_danger = True
                    logger.info(f"NOT PASSED {coin_name}: Risks Single Owner Ownership: {value}")

                # if level == "danger":
                #     self.risk_danger == True
                # elif level == "warn":
                #     self.risk_warn == True

            self.risk_score = _response.get("score", None)
            logger_2.info(f"Rug Check Risks: {self.risk_score} \n {risks}")

        except Exception as e:
            logger.error(f"Rug Check Error: {e}")


