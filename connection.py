import sqlite3
from sqlite3 import Error
from config import Config

def create_connection():
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(Config.DATABASE)
        return conn
    except Error as e:
        print(e)
    return conn