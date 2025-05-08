import sqlite3

class Database:
    def __init__(self, db_name="pessoas.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pessoa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                email TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def get_connection(self):
        return self.connection

    def close(self):
        self.connection.close()
