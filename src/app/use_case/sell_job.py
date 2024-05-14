import asyncio
from asgiref.sync import sync_to_async
import logging

from src.app.services.telegram import Telegram
from src.app.services.trade import SellTrade
from src.database.orm import Configurations, Portfolio
from src.app.services.database import DatabaseManager

logger = logging.getLogger(__name__)


async def job():
    telegram = Telegram()
    db = DatabaseManager()
    configs = await db.get_last_record(entity=Configurations)
    sol = await db.get_record(entity=Portfolio, id=1)  # Solana Amount

    trade = SellTrade(
        expected_profit=configs.expected_profit,
        sell_slippage_rate=configs.sell_slippage_rate,
        solana_wallet_address=configs.solana_wallet_address,
    )

    portofolio_holdings = db.get_all(entity=Portfolio, in_hold=True)
    for hold_coin in portofolio_holdings:

        current_swap_rate = await trade.current_swap_rate(wallet_coin=hold_coin)

        profit = trade.calculate_profit(
            wallet_coin=hold_coin, swap_response=current_swap_rate, configs=configs
        )
        if not profit:
            continue

        new_trade = await trade.sell_coin(swap_response=current_swap_rate)

        hold_coin.sold_at = new_trade.execution_price
        hold_coin.in_hold = False
        hold_coin.profit = trade.profit

        sol.amount += new_trade.coin_amount  # Add amount of sol into account

        db.insert_record(hold_coin)
        db.insert_record(sol)

        print("Transaction ID:")
        logger.info(
            f" COIN Sold: \n"
            f"Bought At: {hold_coin.bought_at}\n"
            f"Sold At: {hold_coin.sold_at}\n"
            f"Profit: {hold_coin.profit}\n"
            f"Fee: {new_trade.fee}\n"
            f"Platform Fee: {new_trade.platformFee}\n"
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(job())
