import requests
import certifi
from app.entity.rug_check import RugCheckEntity


class RugCheck:
    """Scrape info for coins"""

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

    def rug_check(self, mint_address):

        response = requests.get(
            url=f"{self.url}/{mint_address}/report",
            headers=self.headers,
            verify=self.ca_bundle_path,
        )
        return RugCheckEntity(response)
