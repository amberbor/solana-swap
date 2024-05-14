import asyncio
import time

from solders.keypair import Keypair
from solanatracker import SolanaTracker
from src.database.transactions import Transactions
from src.app.entity import TradePairEntity
from src.rugcheck.scan_coin import RugChecker
from src.configs import SOLANA_TRACKER_URL, KEYPAIR, RPC, PAYER_PUBLIC_KEY

import logging

logger = logging.getLogger(__name__)


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

    async def calculate_swap_coin(self, coin_info, nr_holders: int) -> bool:
        """Calculates & Decides based on coin_ information / Configs if to buy or not this coin"""

        try:
            if (
                self.dev_percentage_min
                <= coin_info.dev_percentage
                <= self.dev_percentage_max
            ):
                if 3000 <= coin_info.cap <= 5000:
                    if nr_holders <= 2:
                        logger.info("Coin PASSED checks to trade...")
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


async def main():
    while True:
        start_time = time.time()

        trade = Trade()
        db = Transactions()
        transactions = await db.get_bought_coins()
        await trade.calculate_rates_for_coin_addresses(transactions)

        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time for trade:", execution_time, "seconds")

        await asyncio.sleep(10)


if __name__ == "__maixn__":
    asyncio.run(main())
