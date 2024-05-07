import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB_NAME = os.getenv("POSTGRES_NAME")
POSTGRES_DB_USER = os.getenv("POSTGRES_USERNAME")
POSTGRES_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB_PORT = os.getenv("POSTGRES_PORT")


# TELEGRAM
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_API = os.getenv("API_TELEGRAM")
TELEGRAM_HASH = os.getenv("HASH_TELEGRAM")
TELEGRAM_PHONE_NUMBER = os.getenv("PHONE_NUMBER")

SOLANA_TRACKER_URL = os.getenv("SOLANA_TRACKER_URL")
SOLANA_WALLET_ADDRESS = os.getenv("SOLANA_WALLET_ADDRESS")
AMOUNT_TO_BUY = float(os.getenv("AMOUNT_TO_BUY"))
SLIPPAGE_RATE = float(os.getenv("SLIPPAGE_RATE"))
KEYPAIR = os.getenv("KEYPAIR")
RPC = os.getenv("KEYPAIR")

RUG_CHECK_URL = os.getenv("RUG_CHECK_URL")

TEST = os.getenv("TEST", False)