import os
import sys
from asgiref.sync import sync_to_async

# sys.path.append("/Users/seharborici/solana-swap/src/")
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
# import django
#
# django.setup()

from src.app.services.telegram import Telegram
from src.app.services.trade import Trade
from src.app.services.database import DatabaseManager


# django
async def job():
    telegram = Telegram()
    db = DatabaseManager()
    conf = await sync_to_async(db.get_configurations)()
    trade = Trade(
        dev_percentage_min=conf.dev_percentage_min,
        dev_percentage_max=conf.dev_percentage_max,
        current_holders=conf.current_holders,
        capital_coin=conf.capital_coin
    )
    async for coin_info in telegram.read_messages():
        if await trade.calculate_swap_coin(coin_info):
            coin_db = db.insert_record(coin_info)
            if not coin_db:
                continue

            # trade.


if __name__ == "__main__":
    import asyncio
    asyncio.run(job())
