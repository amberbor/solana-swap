import asyncio
from solders.keypair import Keypair
from meme_api.app.services.solanatracker import SolanaTracker
from meme_api.configs import SOLANA_TRACKER_URL, KEYPAIR, PAYER_PUBLIC_KEY


class Trade:

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
