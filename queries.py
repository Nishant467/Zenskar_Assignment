CREATE_CUSTOMER_TABLE = """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(25),
            email VARCHAR(50) UNIQUE,
            stripe_customer_id VARCHAR (25)
        )
        """

CREATE_SETTINGS_TABLE = """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            key VARCHAR(50) UNIQUE,
            value VARCHAR(50)
        )
        """

ADD_CUSTOMER = "INSERT INTO customers (name, email) VALUES (?, ?)"
SET_CUSTOMER_STRIPE_ID = "UPDATE customers SET stripe_customer_id = ? WHERE id = ?"
GET_CUSTOMER_FROM_ID = "SELECT name, email FROM customers WHERE ID = ?"
UDPATE_CUSTOMER = "UPDATE customers SET name = ?, email = ? WHERE id = ?"
GET_CUSTOMER_FROM_STRIPE_ID = "SELECT stripe_customer_id FROM customers WHERE id = ?"
UPDATE_CUSTOMER_WITH_STRIPE_ID = """
            UPDATE customers
            SET name = ?, email = ?
            WHERE stripe_customer_id = ?
        """

GET_LAST_CHECKED_TIME= "SELECT value FROM settings WHERE key = 'last_checked'"
UPDATE_SETTING = "UPDATE settings SET value = ? WHERE key = 'last_checked'"