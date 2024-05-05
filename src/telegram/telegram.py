import asyncio
import os
import re
import time
from src.configs import HASH_TELEGRAM, API_TELEGRAM, PHONE_NUMBER_TELEGRAM
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from src.database.transactions import Transactions
from src.app.entity import Trade

load_dotenv()

class Message:
    def __init__(self, **kwargs):
        self.mint_address = kwargs.get('mint_address')
        self.name = kwargs.get('name')
        self.symbol = kwargs.get('symbol')
        self.creator = kwargs.get('creator')
        self.cap = kwargs.get('cap')
        self.dev_percentage = kwargs.get('dev_percentage', "0%")
        self.bought = kwargs.get('bought')

class TelegramMessageFetcher:
    attribute_map = {
        'Mint': 'mint_address',
        'Name': 'name',
        'Symbol': 'symbol',
        'Creator': 'creator',
        'Cap': 'cap',
        'Dev': 'dev_percentage',
        'Bought': 'bought'
    }

    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)
        self.transactions = Transactions()
        self.last_message_id = None
        self.trade = Trade()

    async def fetch_messages(self, chat_id, output_file, limit=100):
        await self.client.connect()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        while True:

            if self.last_message_id is not None:
                messages = await self.client.get_messages(chat_id, min_id=self.last_message_id, limit=100)
            else:
                messages = await self.client.get_messages(chat_id, limit=100)

            if messages:
                for message in reversed(messages):
                    msg = self.parse_message(message)
                    if await self.trade.calculate_swap_coin(msg):
                        new_coin_id = self.transactions.add_new_record("coins", msg.__dict__)
                        await self.trade.calculate_rate_coin(msg.mint_address, process="buy", new_coin_id=new_coin_id)

                self.last_message_id = messages[-1].id
                print(f"All messages from chat {chat_id} saved to {output_file}.")
            else:
                print("No new messages found.")

    def parse_message(self, message):
        kwargs = {}
        for line in message.raw_text.split('\n'):
            if line.strip():
                key, value = line.split(': ', 1)
                key = key.split(' ')[-1]
                if key in self.attribute_map:
                    if key == 'Dev' or key == 'Whale':
                        percentage = re.search(r'[\d.]+%', value)
                        if percentage:
                            value_group = percentage.group()
                            if value_group == '0%':
                                value = "0"
                            else:
                                value = value_group.replace("%", "")

                        else:
                            value = "0"
                    elif key == 'Cap':
                        value = value.replace("$", "")
                    kwargs[self.attribute_map[key]] = value.strip("`")
        return Message(**kwargs)

async def main():
    fetcher = TelegramMessageFetcher(API_TELEGRAM, HASH_TELEGRAM, PHONE_NUMBER_TELEGRAM)

    chat_id = int(os.getenv("CHAT_ID"))
    output_file = "telegram.json"

    while True:
        start_time = time.time()

        await fetcher.fetch_messages(chat_id, output_file)

        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time for telegram:", execution_time, "seconds")

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())

