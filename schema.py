from connection import create_connection
from queries import *
def setup_database():
    conn = create_connection()

    if conn is not None:
        cursor = conn.cursor()
        # Create tables
        cursor.execute(CREATE_CUSTOMER_TABLE)
        cursor.execute(CREATE_SETTINGS_TABLE)
        # Initialize last_checked setting if not exists
        cursor.execute("INSERT OR IGNORE INTO settings (id, key, value) VALUES (1, 'last_checked', '0')")
        conn.commit()
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    setup_database()    