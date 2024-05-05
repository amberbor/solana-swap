import base64
import time
import requests
from solders.keypair import Keypair
from solders.transaction import Transaction
from solders.signature import Signature
from solana.rpc.api import Client
from src.configs import SOLANA_TRACKER_URL
import logging

logger = logging.getLogger(__name__)

class SolanaTracker:

    def __init__(self, keypair: Keypair, rpc: str, debug: bool = False):
        self.base_url = SOLANA_TRACKER_URL
        self.connection = Client(rpc)
        self.keypair = keypair
        self.debug = debug

    async def get_rate(self, from_token: str, to_token: str, amount: float, slippage: float) -> dict:
        params = {
            "from": from_token,
            "to": to_token,
            "amount": str(amount),
            "slippage": str(slippage),
        }
        url = f"{self.base_url}/rate"
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as error:
            print("Error fetching rate:", error)
            raise error