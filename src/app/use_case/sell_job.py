import asyncio
from app.services.trade import SellTrade
from database.orm import Configurations, Portfolio
from app.services.database import DatabaseManager

from custom_logger import logger


async def job():
    # telegram = Telegram()
    db = DatabaseManager()
    configs = db.get_last_record(entity=Configurations)
    sol = db.get_record(entity=Portfolio, id=1)  # Solana Amount
    sol_wallet_address = sol.coin.mint_address

    trade = SellTrade(
        expected_profit=configs.expected_profit,
        sell_slippage_rate=configs.sell_slippage_rate,
        solana_wallet_address=sol_wallet_address,
    )

    portofolio_holdings = db.get_all(entity=Portfolio, in_hold=True)
    for wallet_coin in portofolio_holdings:

        current_swap = await trade.current_swap_rate(wallet_coin=wallet_coin)

        swap = trade.calculate_profit(
            wallet_coin=wallet_coin, current_swap=current_swap, configs=configs
        )
        if not swap:
            continue

        new_trade = await trade.sell_coin(current_swap=current_swap)

        wallet_coin.sold_at = new_trade.execution_price
        wallet_coin.in_hold = False
        wallet_coin.profit = trade.profit

        sol.amount += new_trade.amount_out  # Add amount of sol into account

        new_wallet_coin = db.insert_record(wallet_coin)
        db.insert_record(sol)

        print("Transaction ID:")
        logger.info(
            f" COIN Sold: \n"
            f"Bought At: {new_wallet_coin.bought_at}\n"
            f"Sold At: {new_wallet_coin.sold_at}\n"
            f"Profit: {new_wallet_coin.profit}\n"
            f"Fee: {new_trade.fee}\n"
            f"Platform Fee: {new_trade.platform_fee}\n"
        )


if __name__ == "__main__":
    asyncio.run(job())
