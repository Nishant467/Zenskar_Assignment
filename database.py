# database.py
import sqlite3
from sqlite3 import Error
from config import Config

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(Config.DATABASE)
        return conn
    except Error as e:
        print(e)

def setup_database():
    conn = create_connection()
    cursor = conn.cursor()
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        stripe_customer_id TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        key TEXT UNIQUE,
        value TEXT
    )
    """)
    # Initialize last_checked setting if not exists
    cursor.execute("INSERT OR IGNORE INTO settings (id, key, value) VALUES (1, 'last_checked', '0')")
    conn.commit()
    conn.close()
