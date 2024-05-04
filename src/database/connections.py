import os
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    def __init__(self):
        """
        Initializes the DatabaseManager class with database connection parameters.
        """
        self.db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }
        self.connection_pool = self.create_pool()

    def create_pool(self):
        """
        Creates a connection pool for managing database connections.
        """
        return pool.SimpleConnectionPool(1, 10, **self.db_params)

    def get_connection(self):
        """
        Retrieves a connection from the connection pool.
        """
        return self.connection_pool.getconn()

    def close_connection(self, conn):
        """
        Closes a database connection and returns it to the connection pool.
        """
        conn.cursor().close()
        self.connection_pool.putconn(conn)
