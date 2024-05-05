import os
from psycopg2 import pool
from dotenv import load_dotenv
from src.configs import (
    POSTGRES_DB_NAME,
    POSTGRES_DB_HOST,
    POSTGRES_DB_USER,
    POSTGRES_DB_PASSWORD,
    POSTGRES_DB_PORT
)
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.host = POSTGRES_DB_HOST
        self.dbname = POSTGRES_DB_NAME
        self.dbuser = POSTGRES_DB_USER
        self.dbpassword = POSTGRES_DB_PASSWORD
        self.port = POSTGRES_DB_PORT
        self.uri = None
        self.db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }
        self.connection_pool = self.create_pool()

    def create_uri(self):
        if self.uri:
            return self.uri
        self.uri = f"postgresql://{self.dbuser}:{self.dbuser}@{self.host}:{self.port}/{self.dbname}?sslmode=prefer"

    def create_pool(self):
        return pool.SimpleConnectionPool(1, 10, **self.db_params)

    def get_connection(self):
        return self.connection_pool.getconn()

    def close_connection(self, conn):
        conn.cursor().close()
        self.connection_pool.putconn(conn)


# connection_pool = create_pool()
#
# conn = get_connection(connection_pool)
#
# try:
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM my_table")
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)
# finally:
#     close_connection(connection_pool, conn, cur)
