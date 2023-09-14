import datetime
import sqlite3
import os


class usage_db:
    
    def create_tables():
        DB_FILE = os.path.join(os.path.dirname(__file__), 'chats.db') 
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # Create table to store chats 
        c.execute('''
                CREATE TABLE IF NOT EXISTS chat_logs
                (message_id INTEGER PRIMARY KEY, 
                chat_id TEXT,
                message TEXT
                )
                ''')

        conn.commit()
        conn.close()
        # open(DB_FILE, 'w').close()

    def log_new_chat(message_id, chat_id, message):
        DB_FILE = os.path.join(os.path.dirname(__file__), 'chats.db') 
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO chat_logs (message_id, chat_id, message) VALUES (?, ?, ?)', 
                    (message_id, chat_id, message))
            conn.commit()
            conn.close()
            print('Successfully logged data')
        except Exception as e:
            print(f"Error logging to database: {e}") # Print any database errors
            sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
            c.execute(sql_query)
            print(c.fetchall())



    # Usage:
    # After creating a new chat in Telegram, call:
    # log_new_chat(new_chat_id)

    # This will log each new chat and timestamp to the local database

try:
    usage_db.create_tables()
    DB_FILE = os.path.join(os.path.dirname(__file__), 'chats.db') 
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
    c.execute(sql_query)
    print(c.fetchall())
    c.execute(sql_query)
    print(c.fetchall())
except Exception as e:
    print(f'Error: {e}')