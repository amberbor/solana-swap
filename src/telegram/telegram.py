import asyncio
import json
import os
import re
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from src.database.transactions import Transactions

load_dotenv()
class Message:
    def __init__(self, mint=None, name=None, symbol=None, creator=None, dev_percentage=None, bought=False, cap=None):
        self.mint = mint
        self.name = name
        self.symbol = symbol
        self.creator = creator
        self.cap = cap
        self.dev_percentage = dev_percentage
        self.bought = bought

class TelegramMessageFetcher:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)
        self.transactions = Transactions()

    async def fetch_messages(self, chat_id, output_file):
        await self.client.connect()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        last_message_id = (await self.client.get_messages(chat_id, limit=1))[0].id

        while True:
            print("Checking for messages and forwarding them...")

            messages = await self.client.get_messages(chat_id, min_id=last_message_id, limit=None)

            for message in reversed(messages):
                msg = self.parse_message(message)
                self.transactions.add_new_record("messages", msg.__dict__)

            print(f"All messages from chat {chat_id} saved to {output_file}.")


    def parse_message(self, message):
        msg = Message()
        for line in message.raw_text.split('\n'):
            if line.strip():
                key, value = line.split(': ', 1)
                key = key.split(' ')[-1]
                if key == 'Dev' or key == 'Whale':
                    percentage = re.search(r'[\d.]+%', value)
                    if percentage:
                        value = percentage.group()
                setattr(msg, key.strip(), value.strip("`"))
        return msg
async def main():
    fetcher = TelegramMessageFetcher(os.getenv("API_TELEGRAM"), os.getenv("HASH_TELEGRAM"), os.getenv("PHONE_NUMBER"))

    chat_id = int(os.getenv("CHAT_ID"))
    output_file = "telegram.json"

    await fetcher.fetch_messages(chat_id, output_file)


if __name__ == "__main__":
    asyncio.run(main())