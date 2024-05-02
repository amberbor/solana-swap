import os
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }
        self.connection_pool = self.create_pool()

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
