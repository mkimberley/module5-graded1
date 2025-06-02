import sqlite3
import logging

class DBOperations:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def execute_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        logging.info(f"Executed schema query: {query.strip()}")
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()

    def check_populated(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='flights';"
        cursor = self.execute_query(query)
        return cursor.fetchone() is not None
    
    def check_table_exists(self, table_name):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        cursor = self.execute_query(query, (table_name,))
        return cursor.fetchone() is not None
   