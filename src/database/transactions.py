from datetime import datetime

from .connections import DatabaseManager

class Transactions:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_record_by_mint_address(self, table_name, mint_address):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table_name} WHERE mint_address = %s", (mint_address,))
            record = cur.fetchone()
            return record
        finally:
            self.db_manager.close_connection(conn)

    def get_record_by_id(self, table_name, id):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table_name} WHERE id = %s", (id,))
            record = cur.fetchone()
            return record
        finally:
            self.db_manager.close_connection(conn)

    def get_record_by_coin_id(self, coin_id):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM transactions WHERE coin_id = %s", (coin_id,))
            record = cur.fetchone()
            return record
        finally:
            self.db_manager.close_connection(conn)

    def update_transaction_by_id(self, record_id, ammountOut, profit):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            update_query = """
                UPDATE transactions 
                SET price_updated = %s, profit = %s, updated_at = %s
                WHERE id = %s
            """

            updated_at = datetime.now()
            cur.execute(update_query, (ammountOut, profit, updated_at, record_id))
            conn.commit()
            print("Record updated successfully!")
        finally:
            self.db_manager.close_connection(conn)

    def add_new_record(self, table_name, new_record):
        mint_address = new_record.get("mint_address")
        existing_record = self.get_record_by_mint_address(table_name, mint_address)

        if existing_record:
            print(f"A coin with the same mint address already exists in the database : {mint_address}")
            return  # Exit without adding a new record

        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            insert_query = f"INSERT INTO {table_name} ({', '.join(new_record.keys())}) VALUES ({', '.join(['%s'] * len(new_record))}) RETURNING id"
            values = list(new_record.values())
            print("Insert query:", insert_query)
            print("Values:", values)
            cur.execute(insert_query, values)
            affected_rows = cur.rowcount
            if affected_rows > 0:
                new_coin_id = cur.fetchone()[0]
                conn.commit()
                print("New record added successfully!")
                return new_coin_id
            else:
                print("No rows were affected by the INSERT operation. The record may not have been inserted.")
                conn.rollback()
                return None
        except Exception as e:
            print("Error occurred during the INSERT operation:", e)
            conn.rollback()
            return None
        finally:
            self.db_manager.close_connection(conn)

    def add_new_record_transactions(self, table_name, new_record , new_coin_id):
        existing_record = self.get_record_by_coin_id(new_coin_id)

        if existing_record:
            print("A coin with the same mint address already exists in the database.")
            return  # Exit without adding a new record

        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            insert_query = f"INSERT INTO {table_name} (price_sol, coin_id, price_bought, price_updated, profit, sold,mint_address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(insert_query, (new_record['amountIn'], new_coin_id, new_record['amountOut'], new_record['amountOut'], 0, False, new_record['quoteCurrency']['mint']))
            conn.commit()
            print("New record added successfully!")
        finally:
            self.db_manager.close_connection(conn)

    def add_multiple_records(self, table_name, records):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            insert_query = f"INSERT INTO {table_name} ({', '.join(records[0].keys())}) VALUES ({', '.join(['%s'] * len(records[0]))})"
            cur.executemany(insert_query, [list(record.values()) for record in records])
            conn.commit()
            print("Multiple records added successfully!")
        finally:
            self.db_manager.close_connection(conn)

    async def get_bought_coins(self):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM transactions WHERE sold = FALSE")
            records = cur.fetchall()
            transactions = []
            for record in records:

                transaction = {
                    'id': record[0],
                    'price_sol': record[1],
                    'coin_id': record[2],
                    'price_bought': record[3],
                    'price_updated': record[4],
                    'profit': record[5],
                    'sold': record[6],
                    'created_at': record[7],
                    'updated_at': record[8],
                    'mint_address': record[9],
                }
                transactions.append(transaction)

            return transactions
        finally:
            self.db_manager.close_connection(conn)

    def update_transaction_to_sold(self, record_id):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            update_query = """
                UPDATE transactions 
                SET sold = %s
                WHERE id = %s
            """

            cur.execute(update_query, (True, record_id))
            conn.commit()
            print("Sold coin successfully updated!")
        finally:
            self.db_manager.close_connection(conn)



