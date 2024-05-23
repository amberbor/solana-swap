from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors.rpcbaseerrors import UnauthorizedError
from telethon.errors.rpcerrorlist import AuthKeyUnregisteredError
import logging
import aioconsole
from configs import (
    TELEGRAM_API,
    TELEGRAM_HASH,
    TELEGRAM_PHONE_NUMBER,
    TELEGRAM_CHAT_ID,
    TELEGRAM_STRING_KEY,
)
from app.entity.coin_info import CoinInfoEntity

logger = logging.getLogger(__name__)


class Telegram:
    def __init__(self):
        self.chat_id = TELEGRAM_CHAT_ID
        self.api_id = TELEGRAM_API
        self.api_hash = TELEGRAM_HASH
        self.phone_number = TELEGRAM_PHONE_NUMBER
        self.client = TelegramClient(
            StringSession(TELEGRAM_STRING_KEY),
            api_id=self.api_id,
            api_hash=self.api_hash,
        )
        self.last_message_id = None

    async def connect(self):
        try:
            await self.client.connect()
            b = self.client.is_connected()
            is_authorized = await self.client.is_user_authorized()
            if not is_authorized:
                print("Unauthorized")
            #     await self.re_login()
        except (UnauthorizedError, Exception, AuthKeyUnregisteredError) as e:
            logger.warning(f"Unauthorized: Account {self.api_id} is unauthorized !")
            await self.re_login()

    async def read_messages(self):
        # b = await self.client.start()
        await self.connect()
        async for message in self.client.iter_messages(int(self.chat_id)):
            # break if
            if message.id > self.last_message_id:
                yield CoinInfoEntity(message)

    async def re_login(self):
        logger.info(f"Login Retry: Account for account {self.api_id} !")
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            code_input = await aioconsole.ainput("Enter your name: ")
            await self.client.sign_in(self.phone_number, code_input)

    async def new_messages(self, func):
        with TelegramClient(
            "session_" + self.phone_number, api_id=self.api_id, api_hash=self.api_hash
        ) as client:

            @client.on(events.NewMessage())
            async def handler(event):
                await func()

            client.run_until_disconected()
