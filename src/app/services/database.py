import os
from django.db import IntegrityError
from src.configs import (
    POSTGRES_DB_NAME,
    POSTGRES_DB_HOST,
    POSTGRES_DB_USER,
    POSTGRES_DB_PASSWORD,
    POSTGRES_DB_PORT,
TEST
)
from api.models import Coins, Configurations


class DatabaseManager:
    def __init__(self):
        self.host = POSTGRES_DB_HOST
        self.dbname = POSTGRES_DB_NAME
        self.dbuser = POSTGRES_DB_USER
        self.dbpassword = POSTGRES_DB_PASSWORD
        self.port = POSTGRES_DB_PORT
        self.uri = None

    def create_uri(self):
        if self.uri:
            return self.uri
        self.uri = f"postgresql://{self.dbuser}:{self.dbuser}@{self.host}:{self.port}/{self.dbname}?sslmode=prefer"

    def insert_record(self, coin_info):
        try:
            coin = Coins(
                message_id=coin_info.message_id,
                mint_address=coin_info.mint_address,
                name=coin_info.name,
                symbol=coin_info.symbol,
                creator=coin_info.creator,
                cap=coin_info.cap,
                dev_percentage=coin_info.dev_percentage,
                bought=coin_info.bought,
                sent_at=coin_info.sent_at,
            )
            return coin
        except IntegrityError:
            return False

    def get_configurations(self):
        return Configurations.objects.order_by("-id").last()
