import asyncio

from app.services.telegram import Telegram, events, TELEGRAM_CHAT_ID
from app.services.trade import BuyTrade
from app.services.database import DatabaseManager
from app.entity import PortofolioEntity
from app.services.rug_check import RugCheck
from database.orm import Configurations, Portfolio
from app.entity import CoinInfoEntity

from custom_logger import logger


class BuyTradingBot:
    telegram = Telegram()
    db = DatabaseManager()
    rug_check = RugCheck()

    def __init__(self):
        self.configs = None
        self.trade = None

        configs = self.db.get_last_record(entity=Configurations)
        self.trade = BuyTrade(
            dev_percentage_min=configs.dev_percentage_min,
            dev_percentage_max=configs.dev_percentage_max,
            current_holders=configs.current_holders,
            market_cap_min=configs.market_cap_min,
            market_cap_max=configs.market_cap_max,
            amount_to_buy=configs.amount_to_buy,
            buy_slippage_rate=configs.buy_slippage_rate,
            solana_wallet_address=configs.solana_wallet_address,
        )
        self.configs = configs

        # Get the SOL Balance
        self.sol = self.db.get_record(entity=Portfolio, id=1)

    async def job(self, event):
        configs = self.configs

        # holders = await rug_checker.check_rug(coin_info.mint_address)
        holders = 1
        available_amount = self.sol > 0
        coin = CoinInfoEntity(event.message)

        logger.info("---------------------------------------------------------\n")
        logger.info(f"Checking for :\n {str(coin.name)}")
        logger.info(
            f"DEV % : {str(coin.dev_percentage)} ---- CAP : {coin.cap} ---- HOLDR : {holders}"
        )

        coin_mint_address = coin.mint_address
        passed_checks = self.rug_check.rug_check(coin_mint_address).pass_checks

        if passed_checks and available_amount:
            if await self.trade.calculate_swap_coin(coin, holders):
                trade = await self.trade.buy_coin(token_mint_address=coin_mint_address)

                coin_db = coin.db_entity()

                trade.coin = coin
                trade.holders = holders
                trade.traded = True

                portofolio = PortofolioEntity(
                    trade_pair=trade, coin_info=coin, buy_type=True
                )

                portofolio_db = portofolio.db_entity(coin_db=coin_db)

                try:
                    self.db.insert_record(new_record=portofolio_db)
                except Exception as e:
                    pass

                self.sol.amount = self.sol.amount - trade.amount_in  # Update Amount
                self.db.insert_record(self.sol)

                logger.info(
                    f"Transaction ID:, {coin.name}\n"
                    f" COIN BOUGHT: \n"
                    f"Paid Amount: {trade.amount_in}\n"
                    f"Received Amount: {trade.amount_out}\n"
                    f"Price: {trade.execution_price}\n"
                    f"Fee: {trade.fee}\n"
                    f"Platform Fee: {trade.platform_fee}\n"
                )

    async def run(self):
        self.telegram.client.add_event_handler(
            self.job, events.NewMessage(chats=TELEGRAM_CHAT_ID)
        )
        await self.telegram.client.start()
        await self.telegram.client.run_until_disconnected()


bot = BuyTradingBot()

asyncio.run(bot.run())
