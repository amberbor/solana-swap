from asgiref.sync import sync_to_async
# import sys, os

# sys.path.append("/Users/seharborici/solana-swap/src/")
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
# import django
#
# django.setup()
from src.app.services.telegram import Telegram
from src.app.services.trade import Trade
from src.app.services.database import DatabaseManager
from src.app.services.rug_check import RugChecker
from src.database.orm import Configurations

def get_configurations(db_manager: DatabaseManager):
    with db_manager as db:
        return db.get_last_record(entity = Configurations, order_by_field='created_at')

# django
async def job():
    telegram = Telegram()
    db = DatabaseManager()
    conf = await sync_to_async(get_configurations)(db)
    trade = Trade(
        dev_percentage_min=conf.dev_percentage_min,
        dev_percentage_max=conf.dev_percentage_max,
        current_holders=conf.current_holders,
        capital_coin=conf.capital_coin
    )
    async for coin_info in telegram.read_messages():
        holders = await RugChecker().check_rug(coin_info.mint_address)
        if await trade.calculate_swap_coin(coin_info=coin_info, nr_holders=holders):
            coin_db = db.insert_record(coin_info)
            if not coin_db:
                continue
            trade.get_current_coin_price()
            trade.buy_token()


            # trade.


if __name__ == "__main__":
    import asyncio
    asyncio.run(job())
