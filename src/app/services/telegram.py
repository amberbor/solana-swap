
from telethon.sync import TelegramClient, events
from telethon.errors.rpcbaseerrors import UnauthorizedError
import logging
from src.configs import TELEGRAM_API, TELEGRAM_HASH, TELEGRAM_PHONE_NUMBER, TELEGRAM_CHAT_ID
from src.app.entity.message import Message
logger = logging.getLogger(__name__)


class Telegram:
    def __init__(self):
        self.chat_id = TELEGRAM_CHAT_ID
        self.api_id = TELEGRAM_API
        self.api_hash = TELEGRAM_HASH
        self.phone_number = TELEGRAM_PHONE_NUMBER
        self.client = TelegramClient('session_' + self.phone_number, self.api_id, self.api_hash)

    async def connect(self):
        try:
            await self.client.connect()
        except UnauthorizedError as e:
            logger.warning(f"Unauthorized: Account {self.api_id} is unauthorized !")
            await self.re_login()

    async def read_messages(self, last_message_id=0):
        await self.connect()
        async for message in self.client.iter_messages(self.chat_id):
            if message.id > last_message_id:
                yield Message(message)


    async def re_login(self):
        logger.info(f"Login Retry: Account for account {self.api_id} !")
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

    async def new_messages(self, func):
        with TelegramClient('session_' + self.phone_number, api_id=self.api_id, api_hash=self.api_hash) as client:

            @client.on(events.NewMessage())
            async def handler(event):
                await func()

            client.run_until_disconected()
