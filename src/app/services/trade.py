import asyncio
import time
from datetime import datetime

from solders.keypair import Keypair
from solanatracker import SolanaTracker
from dotenv import load_dotenv
from src.database.transactions import Transactions
from src.rugcheck.scan_coin import RugChecker
import os
from src.configs import SOLANA_TRACKER_URL, SOLANA_WALLET_ADDRESS, AMOUNT_TO_BUY, SLIPPAGE_RATE, KEYPAIR, RPC


class Trade:
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
        self.ammountIn = None
        self.ammountOut = None
        self.minAmountOut = None
        self.currentPrice = None
        self.executionPrice = None
        self.priceImpact = None
        self.isPumpFun = None
        self.platformFee = None
        self.fee = None
        self.baseCurrency = None
        self.quoteCurrency = None
        self.tokenBought = None
        self.db = Transactions()
        self.rug_check = RugChecker()

        self._keypair = Keypair.from_base58_string(self.KEYPAIR)

    async def calculate_rate_coin(
        self, coin_address, process=None, new_coin_id=None, transaction=None
    ) -> dict:
        solana_tracker = SolanaTracker(self.keypair, RPC )

        retry_count = 3
        rate_response = None
        while retry_count > 0:
            try:
                rate_response = await solana_tracker.get_rate(
                   SOLANA_WALLET_ADDRESS, # From Token
                    coin_address,  # To Token
                    float(AMOUNT_TO_BUY),  # Amount to swap
                    float(os.getenv("SLIPPAGE_RATE")),  # Slippage
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
            self.ammountIn = rate_response["amountIn"]
            self.ammountOut = rate_response["amountOut"]
            self.minAmountOut = rate_response["minAmountOut"]
            self.currentPrice = rate_response["currentPrice"]
            self.executionPrice = rate_response["executionPrice"]
            self.priceImpact = rate_response["priceImpact"]
            self.isPumpFun = rate_response["isPumpFun"]
            self.platformFee = rate_response["platformFee"]
            self.fee = rate_response["fee"]
            self.baseCurrency = rate_response["baseCurrency"]["mint"]
            self.quoteCurrency = rate_response["quoteCurrency"]["mint"]

            if process == "buy" and new_coin_id is not None:
                self.db.add_new_record_transactions(
                    "transactions", rate_response, new_coin_id=new_coin_id
                )

            if process == "update" and new_coin_id is not None:
                profit = self.profit_percentage(transaction["price_bought"])
                if profit >= 200:
                    self.db.update_transaction_to_sold(transaction["id"])
                elif profit == 0:
                    self.sell_no_profit(transaction)

                self.db.update_transaction_by_id(
                    new_coin_id, rate_response["amountOut"], profit
                )

        return rate_response

    def sell_no_profit(self, transaction):
        created_at = transaction["created_at"]
        updated_at = transaction["updated_at"]
        time_diff = updated_at - created_at

        if time_diff.total_seconds() >= 120:
            self.db.update_transaction_to_sold(transaction["id"])

    def profit_percentage(self, priceBought):
        return ((self.ammountOut - priceBought) / priceBought) * 100

    async def buy_coin(self) -> dict:
        keypair = Keypair.from_base58_string(os.getenv("PAYER_PUBLIC_KEY"))

        solana_tracker = SolanaTracker(keypair, os.getenv("RPC"))

        swap_response = await solana_tracker.get_swap_instructions(
            os.getenv("SOLANA_WALLET_ADDRESS"),  # From Token
            "47p9s6G7mcAkELaq2kr2xLquLHgoJjEeHdcrf1xJkjnk",  # To Token
            float(os.getenv("AMOUNT_TO_BUY")),  # Amount to swap
            float(os.getenv("SLIPPAGE_SWAP")),  # Slippage
            str(keypair.pubkey()),  # Payer public key
        )

        txid = await solana_tracker.perform_swap(swap_response)

        if not txid:
            raise Exception("Swap failed")

        txid_url = f"https://explorer.solana.com/tx/{txid}"

        swap_response["txid"] = txid
        swap_response["txid_url"] = txid_url

        print("Transaction ID:", txid)
        print("Transaction URL:", f"https://explorer.solana.com/tx/{txid}")

        self.tokenBought = swap_response["rate"]["quoteCurrency"]["mint"]
        self.amountSolana = swap_response["rate"]["amountIn"]
        self.amountTokenBought = swap_response["rate"]["amountOut"]

        return swap_response

    async def sell_coin(self) -> dict:
        keypair = Keypair.from_base58_string(os.getenv("PAYER_PUBLIC_KEY"))

        solana_tracker = SolanaTracker(keypair, os.getenv("RPC"))

        swap_response = await solana_tracker.get_swap_instructions(
            os.getenv("SOLANA_WALLET_ADDRESS"),  # From Token
            "47p9s6G7mcAkELaq2kr2xLquLHgoJjEeHdcrf1xJkjnk",  # To Token
            float(os.getenv("AMOUNT_TO_BUY")),  # Amount to swap
            float(os.getenv("SLIPPAGE_SWAP")),  # Slippage
            str(keypair.pubkey()),  # Payer public key
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

    async def calculate_swap_coin(self, coin_info) -> bool:
        rug_holders = await self.rug_check_holders(coin_info.mint_address)
        if self.dev_percentage_min <= coin_info.dev_percentage <= self.dev_percentage_max:
            if 3000 <= coin_info.cap <= 5000:
                if len(rug_holders) <= 2:
                     return True
        return False

    async def rug_check_holders(self, mint_address):
        return await self.rug_check.check_rug(mint_address)

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


if __name__ == "__main__":
    asyncio.run(main())
