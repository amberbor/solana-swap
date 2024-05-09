import asyncio
import time
from datetime import datetime

from solders.keypair import Keypair
from solanatracker import SolanaTracker
from src.database.transactions import Transactions
from src.rugcheck.scan_coin import RugChecker
from src.app.entity.tradepair import TradePair
from src.app.entity.portofolio import Portofolio
from src.configs import SOLANA_TRACKER_URL, SOLANA_WALLET_ADDRESS, AMOUNT_TO_BUY, SLIPPAGE_RATE, KEYPAIR, RPC, PAYER_PUBLIC_KEY


class Trade:
    rug_check = RugChecker()

    def __init__(
        self,
        dev_percentage_min: float = 1,
        dev_percentage_max: float = 5,
        current_holders: int = 2,
        capital_coin: float = 5000,
    ):
        self.dev_percentage_min = dev_percentage_min
        self.dev_percentage_max = dev_percentage_max
        self.current_holders = current_holders
        self.capital_coin = capital_coin
        self.amount_to_buy = AMOUNT_TO_BUY # config
        self.solana_tracker_url = SOLANA_TRACKER_URL #config

        self.tokenBought = None

        self.solana_tracker_url = SOLANA_TRACKER_URL
        self.solana_wallet_address = SOLANA_WALLET_ADDRESS

        self._keypair = Keypair.from_base58_string(KEYPAIR)
        self.solana_tracker = SolanaTracker()

        self._keypair_payer_public_key = Keypair.from_base58_string(PAYER_PUBLIC_KEY)
        self._public_payer_key =   self._keypair_payer_public_key .pubkey()  # Payer public key



    def check_connection(self):
        if not self.solana_tracker.connection.is_connected:
            self.solana_tracker.reconnect()


    async def get_current_coin_price(
        self, coin_address, new_coin_id=None, transaction=None
    ) -> dict:
        self.check_connection()

        retry_count = 3
        rate_response = None
        while retry_count > 0:
            try:
                rate_response = await self.solana_tracker.get_rate(
                   SOLANA_WALLET_ADDRESS, # From Token
                    coin_address,  # To Token
                    AMOUNT_TO_BUY,  # Amount to swap
                    SLIPPAGE_RATE,  # Slippage
                )
                break  # Exit the loop if successful
            except Exception as e:
                print(f"Error fetching rate: {e}")
                retry_count -= 1
                if retry_count > 0:
                    print(f"Retrying... {retry_count} retries left.")
                    await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    print("No more retries left. Exiting.")

        if rate_response:
            response = TradePair(
                base_coin_amount=rate_response["amountIn"] ,# coin Amount
                coin_amount=rate_response["amountOut"] ,# coin Amount
                min_amount_out=rate_response["minAmountOut"], # coin Amount
                current_price=rate_response["currentPrice"] ,# coin Amount
                execution_price=rate_response["executionPrice"], # coin Amount
                price_impact=rate_response["priceImpact"], # coin Amount
                is_pump_fun=rate_response["isPumpFun"] ,# coin Amount
                platform_fee=rate_response["platformFee"] ,# coin Amount
                base_currency=rate_response["baseCurrency"]["mint"],
                quote_currency=rate_response["quoteCurrency"]["mint"]
            )
            return response

    async def buy_token(self, coin_id):
        '''Buy then update db'''
        pass

        # if process == "buy" and new_coin_id is not None:
        #     self.db.add_new_record_transactions(
        #         "transactions", rate_response, new_coin_id=new_coin_id
        #     )
    async def update_token(self, coin_id):
        '''Check if to sell then update db'''
        pass
            # if process == "update" and new_coin_id is not None:
            #     profit = self.profit_percentage(transaction["price_bought"])
            #     if profit >= 200:
            #         self.db.update_transaction_to_sold(transaction["id"])
            #     elif profit == 0:
            #         self.sell_no_profit(transaction)
            #
            #     self.db.update_transaction_by_id(
            #         new_coin_id, rate_response["amountOut"], profit
            #     )

    def sell_no_profit(self, transaction):
        '''Sell then update db'''
        pass
        # created_at = transaction["created_at"]
        # updated_at = transaction["updated_at"]
        # time_diff = updated_at - created_at
        #
        # if time_diff.total_seconds() >= 120:
        #     self.db.update_transaction_to_sold(transaction["id"])

    def profit_percentage(self, priceBought):
        return ((self.ammountOut - priceBought) / priceBought) * 100

    async def buy_coin(self) -> dict:

        swap_response = await self.solana_tracker.get_swap_instructions(
            SOLANA_WALLET_ADDRESS,  # From Token
            "47p9s6G7mcAkELaq2kr2xLquLHgoJjEeHdcrf1xJkjnk",  # To Token
            AMOUNT_TO_BUY,  # Amount to swap
            SLIPPAGE_RATE,  # Slippage
             self._public_payer_key,
        )

        txid = await self.solana_tracker.perform_swap(swap_response)

        if not txid:
            raise Exception("Swap failed")

        print("Transaction ID:", txid)

        response = Portofolio(
            txid = txid,
            txid_url = f"https://explorer.solana.com/tx/{txid}",
            quote_currency = swap_response["rate"]["quoteCurrency"]["mint"],
            base_currency = swap_response["rate"]["baseCurrency"]["mint"],
            amount = swap_response["rate"]["amountIn"],
            base_amount = swap_response["rate"]["amountOut"]
        )

        #Save to DB
        return response

    async def sell_coin(self) -> dict:
        solana_tracker = SolanaTracker(self._keypair_payer_public_key, RPC)

        swap_response = await solana_tracker.get_swap_instructions(
            SOLANA_WALLET_ADDRESS,  # From Token
            "47p9s6G7mcAkELaq2kr2xLquLHgoJjEeHdcrf1xJkjnk",  # To Token
           AMOUNT_TO_BUY,  # Amount to swap
            SLIPPAGE_RATE,  # Slippage
            self._public_payer_key,
            0.00005,  # Priority fee (Recommended while network is congested)
            True,  # Force legacy transaction for Jupiter
        )

        txid = await solana_tracker.perform_swap(swap_response)

        if not txid:
            raise Exception("Swap failed")

        txid_url = f"https://explorer.solana.com/tx/{txid}"

        swap_response["txid"] = txid
        swap_response["txid_url"] = txid_url

        print("Transaction ID:", txid)
        print("Transaction URL:", f"https://explorer.solana.com/tx/{txid}")

        return swap_response

    async def calculate_swap_coin(self, coin_info, nr_holders:int) -> bool:
        '''Calculates & Decides based on coin_ information if to buy or not this coin'''
        if self.dev_percentage_min <= coin_info.dev_percentage <= self.dev_percentage_max:
            if 3000 <= coin_info.cap <= 5000:
                if len(nr_holders) <= 2:
                     return True
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
