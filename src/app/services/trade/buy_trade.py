from .trade import Trade
from src.app.entity import TradePairEntity
from src.configs import RUN_ENV
from src.custom_logger import logger


class BuyTrade(Trade):

    def __init__(
        self,
        dev_percentage_min: float = 1,
        dev_percentage_max: float = 5,
        current_holders: int = 2,
        capital_coin: float = 5000,
        amount_to_buy: float = None,
        buy_slippage_rate: float = None,
        solana_wallet_address: float = None,
    ):
        self.dev_percentage_min = dev_percentage_min
        self.dev_percentage_max = dev_percentage_max
        self.current_holders = current_holders
        self.capital_coin = capital_coin
        self.amount_to_buy = amount_to_buy
        self.slippage_rate = buy_slippage_rate
        super().__init__(solana_wallet_address)

    async def buy_coin(self, token_mint_address) -> TradePairEntity:

        swap_response = await self.solana_tracker.get_swap_instructions(
            from_token=self.solana_wallet_address,  # From Token
            to_token=token_mint_address,  # To Token
            from_amount=self.amount_to_buy,  # Amount to swap
            slippage=self.slippage_rate,  # Slippage
            payer=self._public_payer_key,
        )

        txid = swap_response["txn"]
        if RUN_ENV == "PROD":
            txid = await self.solana_tracker.perform_swap(swap_response)
        logger.info("Token bought successfully")

        if not txid:
            raise Exception("Swap failed")

        rate_response = swap_response["rate"]

        response = TradePairEntity(
            txid=txid,
            txid_url=f"https://explorer.solana.com/tx/{txid}",
            amount_in=rate_response["amountIn"],  #  Amount of Source Token (Solana)
            amount_out=rate_response["amountOut"],  #  Amount Destination received
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
