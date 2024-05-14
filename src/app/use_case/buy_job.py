import asyncio

from asgiref.sync import sync_to_async

# import sys, os

# sys.path.append("/Users/seharborici/solana-swap/src/")
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
# import django
#
# django.setup()
from src.app.services.telegram import Telegram, events, TELEGRAM_CHAT_ID
from src.app.services.trade import BuyTrade
from src.app.services.database import DatabaseManager
from src.app.entity import PortofolioEntity
from src.app.services.rug_check import RugCheck
from src.database.orm import CoinInfo, TradePair, Portfolio
from src.database.orm import Configurations, Portfolio

import logging

logger = logging.getLogger(__name__)


# @telegram.client.on(events.NewMessage(chats=TELEGRAM_CHAT_ID))
# async def job(event):
#
#     print(events.text)
#     coin_info = event.text
#     logger.info("---------------------------------------------------------\n")
#     logger.info(f"Checking coin :\n {str(coin_info)}")
#     # holders = await rug_checker.check_rug(coin_info.mint_address)
#     holders = 1
#     if await trade.calculate_swap_coin(coin_info=coin_info, nr_holders=holders):
#
#         trade_entity = await trade.buy_coin(token_mint_address=coin_info.mint_address)
#
#         coin = CoinInfo(
#             message_id=coin_info.message_id,
#             mint_address=coin_info.mint_address,
#             name=coin_info.name,
#             symbol=coin_info.symbol,
#             creator=coin_info.creator,
#             cap=coin_info.cap,
#             dev_percentage=coin_info.dev_percentage,
#         )
#
#         # coin_id = db.insert_record(new_record=coin)
#
#         trade_pair = TradePair(
#             coin=coin,
#             base_coin_amount=trade_entity.base_coin_amount,
#             coin_amount=trade_entity.coin_amount,
#             min_amount_out=trade_entity.min_amount_out,
#             current_price=trade_entity.current_price,
#             execution_price=trade_entity.execution_price,
#             price_impact=trade_entity.price_impact,
#             is_pump_fun=trade_entity.is_pump_fun,
#             platform_fee=trade_entity.platform_fee,
#             base_currency=trade_entity.base_currency,
#             quote_currency=trade_entity.quote_currency,
#             updated_at=trade_entity.updated_at,
#             created_at=trade_entity.created_at,
#         )
#
#         # trade_id = db.insert_record(new_record=_tradepair)
#
#         portofolio_entity = PortofolioEntity(
#             trade_pair=trade_entity, coin_info=coin_info, buy_type=True
#         )
#
#         portofolio = Portfolio(
#             trade_pair=trade_pair,
#             coin=coin,
#             amount=portofolio_entity.amount,
#             bought_at=portofolio_entity.bought_at,
#             sold_at=portofolio_entity.sold_at,
#             profit=portofolio_entity.profit,
#             in_hold=portofolio_entity.in_hold,
#         )
#         db.insert_record(new_record=portofolio)
#
#         sol.amount = sol.amount - trade_entity.base_coin_amount  # Update Amount
#         db.insert_record(sol)
#
#         telegram.last_message_id = coin_info.message_id  # Update last message id
#

# async def main():
#     db = DatabaseManager()
#     rug_checker = RugCheck()
#     conf = db.get_last_record(entity=Configurations)
#     sol = db.get_record(entity=Portfolio, id=1)  # Solana Amount
#     last_message = db.get_last_record(entity=CoinInfo)
#     if last_message:
#         telegram.last_message_id = last_message.message_id
#
#     trade = BuyTrade(
#         dev_percentage_min=conf.dev_percentage_min,
#         dev_percentage_max=conf.dev_percentage_max,
#         current_holders=conf.current_holders,
#         capital_coin=conf.capital_coin,
#         amount_to_buy=conf.amount_to_buy,
#         buy_slippage_rate=conf.buy_slippage_rate,
#         solana_wallet_address=conf.solana_wallet_address,
#     )


# telegram.client.run_until_disconnected(main())


class BuyTradingBot:

    def __init__(self, telegram, db_manager):
        self.telegram = telegram
        self.db = db_manager
        self.configs = None
        self.trade = None
        # self.init_trade_cofing()

    async def job(self, event):
        print(event.text)

    def init_trade_cofing(self):
        configs = self.db.get_last_record(entity=Configurations)
        self.trade = BuyTrade(
            dev_percentage_min=configs.dev_percentage_min,
            dev_percentage_max=configs.dev_percentage_max,
            current_holders=configs.current_holders,
            capital_coin=configs.capital_coin,
            amount_to_buy=configs.amount_to_buy,
            buy_slippage_rate=configs.buy_slippage_rate,
            solana_wallet_address=configs.solana_wallet_address,
        )
        self.configs = configs

    async def run(self):
        self.telegram.client.add_event_handler(
            self.job, events.NewMessage(chats=TELEGRAM_CHAT_ID)
        )
        await self.telegram.client.start()
        await self.telegram.client.run_until_disconnected()


telegram = Telegram()
db = DatabaseManager()

bot = BuyTradingBot(telegram, db)

asyncio.run(bot.run())
