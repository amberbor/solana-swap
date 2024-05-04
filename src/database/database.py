import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    try:
        # Connect to the database
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Define the SQL statements for creating tables
        create_coins_table_query = """
            CREATE TABLE IF NOT EXISTS coins (
                id SERIAL PRIMARY KEY,
                mint_address VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                symbol VARCHAR(10) NOT NULL,
                creator VARCHAR(255) NOT NULL,
                cap VARCHAR(255) NOT NULL,
                dev_percentage VARCHAR(255) NOT NULL
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            )
        """

        create_transactions_table_query = """
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                price_sol FLOAT NOT NULL,
                coin_id INT NOT NULL REFERENCES coins(id),
                price_bought FLOAT NOT NULL,
                price_updated FLOAT NOT NULL,
                profit FLOAT NOT NULL,
                sold BOOLEAN NOT NULL
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mint_address VARCHAR(255) NOT NULL,
            )
        """

        # Execute the create table queries
        cursor.execute(create_coins_table_query)
        cursor.execute(create_transactions_table_query)

        # Commit the transaction
        connection.commit()

        print("Tables created successfully!")

    except psycopg2.Error as e:
        print("Error while connecting to PostgreSQL:", e)

    finally:
        # Close the cursor and connection
        if 'connection' in locals():
            cursor.close()
            connection.close()


# Call the function to create tables
create_tables()
