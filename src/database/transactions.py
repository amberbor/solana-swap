import connections

class Transactions:
    def __init__(self):
        self.db_manager = connections.DatabaseManager()

    def get_record_by_id(self, table_name, record_id):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
            record = cur.fetchone()
            return record
        finally:
            self.db_manager.close_connection(conn)

    def update_record_by_id(self, table_name, record_id, new_values):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            update_query = f"UPDATE {table_name} SET "
            update_query += ", ".join([f"{column} = %s" for column, value in new_values.items()])
            update_query += f" WHERE id = %s"
            cur.execute(update_query, list(new_values.values()) + [record_id])
            conn.commit()
            print("Record updated successfully!")
        finally:
            self.db_manager.close_connection(conn)

    def add_new_record(self, table_name, new_record):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            insert_query = f"INSERT INTO {table_name} "
            insert_query += "(" + ", ".join(new_record.keys()) + ") "
            insert_query += "VALUES (" + ", ".join(["%s"] * len(new_record)) + ")"
            cur.execute(insert_query, list(new_record.values()))
            conn.commit()
            print("New record added successfully!")
        finally:
            self.db_manager.close_connection(conn)

    def add_multiple_records(self, table_name, records):
        conn = self.db_manager.get_connection()
        try:
            cur = conn.cursor()
            insert_query = f"INSERT INTO {table_name} "
            insert_query += "(" + ", ".join(records[0].keys()) + ") "
            insert_query += "VALUES (" + ", ".join(["%s"] * len(records[0])) + ")"
            cur.executemany(insert_query, [list(record.values()) for record in records])
            conn.commit()
            print("Multiple records added successfully!")
        finally:
            self.db_manager.close_connection(conn)
