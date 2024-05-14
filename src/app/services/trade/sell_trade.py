import logging
from .trade import Trade
from src.configs import RUN_ENV
import asyncio
from src.app.entity import TradePairEntity
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)


class SellTrade(Trade):
    def __init__(self, expected_profit, sell_slippage_rate, solana_wallet_address):
        self.expected_profit = expected_profit
        self.sell_slippage_rate = sell_slippage_rate
        self.profit = None
        super().__init__(solana_wallet_address)

    async def current_swap_rate(self, wallet_coin) -> TradePairEntity:
        self.profit = None

        swap_response = await self.solana_tracker.get_swap_instructions(
            from_token=wallet_coin.coin.mint_address,  # From Token Try to change
            to_token=self.solana_wallet_address,  # To Token
            from_amount=wallet_coin.amount,  # Amount to swap
            slippage=self.sell_slippage_rate,  # Slippage
            payer=self._public_payer_key,
            priority_fee=0.00005,  # Priority fee (Recommended while network is congested)
            force_legacy=True,  # Force legacy transaction for Jupiter
        )
        return swap_response

    def calculate_profit(self, wallet_coin, swap_response, configs):
        self.profit = 0
        nr_holders = wallet_coin.trade_pair.holders
        now = datetime.now(timezone.utc)

        rate_response = swap_response["rate"]

        current_price = rate_response["executionPrice"]

        price_bought = wallet_coin.bought_at

        # Calculate the minimum price that would yield 2x profit
        double_price = 2 * price_bought

        # Check if the current price is at least twice the price bought
        if current_price >= double_price:
            return True

        if 2 <= nr_holders <= 3:
            if wallet_coin.created_at < now - timedelta(
                seconds=configs.first_wait_seconds
            ):
                return True

        if 3 <= nr_holders <= 4:
            if wallet_coin.created_at < now - timedelta(
                seconds=configs.second_wait_seconds
            ):
                return True

        if 4 <= nr_holders <= 5:
            if wallet_coin.created_at < now - timedelta(
                seconds=configs.third_wait_seconds
            ):
                return True

        return False

    async def sell_coin(self, swap_response):
        rate_response = swap_response["rate"]

        txid = swap_response["txn"]
        if RUN_ENV == "PROD":
            txid = await self.solana_tracker.perform_swap(swap_response)

        if not txid:
            raise Exception("Swap failed")

        response = TradePairEntity(
            txid=txid,
            txid_url=f"https://explorer.solana.com/tx/{txid}",
            base_coin_amount=rate_response[
                "amountIn"
            ],  #  Amount of Source Token (Solana)
            coin_amount=rate_response["amountOut"],  #  Amount Destination received
            min_amount_out=rate_response[
                "minAmountOut"
            ],  # Min Amount  of destination token willing to receive
            current_price=rate_response[
                "currentPrice"
            ],  # Current market price for the Token Pair
            execution_price=rate_response[
                "executionPrice"
            ],  # The actual price the trade will be executed
            price_impact=rate_response[
                "priceImpact"
            ],  # % of the Diff of current_price - execution price (Lack of Liquidity)
            fee=rate_response["fee"],  # Trade fee charged for transaction
            platform_fee=rate_response[
                "platformFee"
            ],  # Trade fee charged for transaction
            platform_fee_ui=rate_response[
                "platformFeeUI"
            ],  # Trade fee charged for transaction
            base_currency=rate_response["baseCurrency"][
                "mint"
            ],  # Fee charged by platform for the transaction
            quote_currency=rate_response["quoteCurrency"][
                "mint"
            ],  # Platform fee in SOL
            is_pump_fun=rate_response["isPumpFun"],  # coin Amount
        )

        return response

    async def get_current_coin_price(
        self, token_mint_address: str, amount: float
    ) -> TradePairEntity:
        self.check_connection()

        retry_count = 3
        rate_response = None
        while retry_count > 0:
            try:
                rate_response = await self.solana_tracker.get_rate(
                    from_token=token_mint_address,  # From Token
                    to_token=self.solana_wallet_address,  # To Token
                    amount=amount,  # Amount to swap
                    slippage=self.sell_slippage_rate,  # Slippage
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
            response = TradePairEntity(
                base_coin_amount=rate_response[
                    "amountIn"
                ],  #  Amount of Source Token (Solana)
                coin_amount=rate_response["amountOut"],  #  Amount Destination received
                min_amount_out=rate_response[
                    "minAmountOut"
                ],  # Min Amount  of destination token willing to receive
                current_price=rate_response[
                    "currentPrice"
                ],  # Current market price for the Token Pair
                execution_price=rate_response[
                    "executionPrice"
                ],  # The actual price the trade will be executed
                price_impact=rate_response[
                    "priceImpact"
                ],  # % of the Diff of current_price - execution price (Lack of Liquidity)
                fee=rate_response["fee"],  # Trade fee charged for transaction
                platform_fee=rate_response[
                    "platformFee"
                ],  # Trade fee charged for transaction
                platform_fee_ui=rate_response[
                    "platformFeeUI"
                ],  # Trade fee charged for transaction
                base_currency=rate_response["baseCurrency"][
                    "mint"
                ],  # Fee charged by platform for the transaction
                quote_currency=rate_response["quoteCurrency"][
                    "mint"
                ],  # Platform fee in SOL
                is_pump_fun=rate_response["isPumpFun"],  # coin Amount
            )
            return response
