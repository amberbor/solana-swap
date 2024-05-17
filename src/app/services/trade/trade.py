import asyncio

from solders.keypair import Keypair
from solanatracker import SolanaTracker
from src.rugcheck.scan_coin import RugChecker
from src.configs import SOLANA_TRACKER_URL, KEYPAIR, RPC, PAYER_PUBLIC_KEY
from src.custom_logger import logger


class Trade:
    rug_check = RugChecker()

    def __init__(self, solana_wallet_address: str = None):

        self.solana_wallet_address = solana_wallet_address

        self.tokenBought = None

        self.solana_tracker_url = SOLANA_TRACKER_URL

        self._keypair = Keypair.from_base58_string(KEYPAIR)
        self.solana_tracker = SolanaTracker()

        self._keypair_payer_public_key = Keypair.from_base58_string(PAYER_PUBLIC_KEY)
        self._public_payer_key = (
            self._keypair_payer_public_key.pubkey()
        )  # Payer public key

    def check_connection(self):
        if not self.solana_tracker.connection.is_connected:
            self.solana_tracker.reconnect()

    async def calculate_swap_coin(self, coin, holders: int) -> bool:
        """
        Calculates & Decides based on coin_ information / Configs if to buy or not this coin
        1. Calculate based on dev percentage
        2. Calculate based on Market Cap
        3. Calculate based on number of coin holders at this time
        """

        try:
            coin_dev_percentage = coin.dev_percentage
            if (
                coin_dev_percentage is not None  # If dev % not determined pass
                and self.dev_percentage_min
                <= coin_dev_percentage
                <= self.dev_percentage_max
            ):
                if 3000 <= coin.cap <= 5000:
                    if holders <= 2:
                        return True
            return False
        except Exception as e:
            logger.info("Coin NOT PASSED checks to trade...")
            return False

    async def calculate_rates_for_coin_addresses(self, transactions) -> list:
        tasks = [
            self.calculate_rate_coin(
                transaction["mint_address"],
                process="update",
                new_coin_id=transaction["id"],
                transaction=transaction,
            )
            for transaction in transactions
        ]
        result_tuples = await asyncio.gather(*tasks)
        return list(result_tuples)
