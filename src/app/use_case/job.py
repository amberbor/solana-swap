import os
import sys
sys.path.append('/Users/seharborici/solana-swap/src/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
import django
django.setup()

import asyncio
from src.app.services.telegram import Telegram
from src.app.services.trade import Trade
from src.app.services.database import DatabaseManager

# django
async def job():
    telegram = Telegram()
    db = DatabaseManager()
    trade = Trade
    async for message in telegram.read_messages():
        if trade.calculate_swap_coin(message):
            record = db.insert_record(message)
            if not record:
                continue
            # trade.



if __name__ == '__main__':
    asyncio.run(job())