import sqlite3
from typing import Literal, Union
from time import time

class Database:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        data = (
            "CREATE TABLE IF NOT EXISTS users(chat_id PRIMARY KEY , time INTEGER);"
            "CREATE TABLE IF NOT EXISTS groups(chat_id PRIMARY KEY , time INTEGER);"
        )
        self.cursor.executescript(data)
        self.conn.commit()
    
    def is_in_table(self, chat_id:str, table_name:Literal['users', 'groups']) -> Union[tuple, None]:
        q = f" SELECT * FROM {table_name} WHERE chat_id=?"
        data = self.cursor.execute(q, (chat_id,))
        data = data.fetchone()
        return data
    
    def insert_or_ignore(self, chat_id:str, table_name:Literal['users', 'groups']):
        q = f"INSERT OR IGNORE INTO {table_name} VALUES(?, ?)" 
        data = (chat_id, int(time())) 
        self.cursor.execute(q, data)
        self.conn.commit()

    def close(self):
        self.conn.close()

