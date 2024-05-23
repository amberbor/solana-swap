from configs import TELEGRAM_API, TELEGRAM_HASH, TELEGRAM_PHONE_NUMBER

print("yes")
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio


client = TelegramClient(
    "src/session_+355699577766.session", TELEGRAM_API, TELEGRAM_HASH
)
asyncio.run(client.send_code_request(TELEGRAM_PHONE_NUMBER))
code = input("code: ")
asyncio.run(client.sign_in(TELEGRAM_PHONE_NUMBER, code))
print(client.session.save())
