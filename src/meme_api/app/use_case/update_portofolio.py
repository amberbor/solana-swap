from asgiref.sync import sync_to_async

from meme_api.app.services.telegram import Telegram
from meme_api.app.services.database import DatabaseManager
from meme_api.app.services.trade import Trade
from meme_api.api.models import Portofolio


async def update_portofolio():
    telegram = Telegram()
    db = DatabaseManager()
    conf = await sync_to_async(db.get_configurations)()
    trade = Trade()
    portofolio = Portofolio.objects.all()
    for item in portofolio:
        trade.calculate_profit()
