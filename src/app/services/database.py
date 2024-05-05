import os
from django.db import IntegrityError
from src.configs import (
    POSTGRES_DB_NAME,
    POSTGRES_DB_HOST,
    POSTGRES_DB_USER,
    POSTGRES_DB_PASSWORD,
    POSTGRES_DB_PORT
)
from api.models import Coins

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


    def insert_record(self, record):
        try:
            coin = Coins(message_id='', mint_address='', name='', symbol='', creator='', cap='', dev_percentage='', bought='')
            return coin
        except IntegrityError:
            return False