import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB_NAME = os.getenv("POSTGRES_NAME")
POSTGRES_DB_USER = os.getenv("POSTGRES_USERNAME")
POSTGRES_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB_PORT = os.getenv("POSTGRES_PORT")


# TELEGRAM
TELEGRAM_CHAT_ID = int(os.getenv("CHAT_ID"))
TELEGRAM_API = os.getenv("API_TELEGRAM")
TELEGRAM_HASH = os.getenv("HASH_TELEGRAM")
TELEGRAM_PHONE_NUMBER = os.getenv("PHONE_NUMBER")

SOLANA_TRACKER_URL = os.getenv("SOLANA_TRACKER_URL")
KEYPAIR = os.getenv("KEYPAIR")
RPC = os.getenv("RPC")

RUG_CHECK_URL = os.getenv("RUG_CHECK_URL")
PAYER_PUBLIC_KEY = os.getenv("PAYER_PUBLIC_KEY")

RUN_ENV = os.getenv("ENVIRONMENT", "TEST")

TELEGRAM_STRING_KEY = os.getenv("TELEGRAM_STRING_KEY")