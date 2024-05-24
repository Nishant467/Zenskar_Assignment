import stripe
import schedule
import time
import sqlite3
from config import Config
from queries import *
# Initialize Stripe API
stripe.api_key = Config.STRIPE_API_KEY

def poll_stripe_customers():
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    # Get the last checked time from your database
    cursor.execute(GET_LAST_CHECKED_TIME)
    last_checked = cursor.fetchone()[0]

    # Assuming last_checked is stored as a Unix timestamp
    # Fetch recent customers from Stripe
    customers = stripe.Customer.list(created={'gte': last_checked})
    for customer in customers.auto_paging_iter():
        print(customer)
        # Update local database with new info
        cursor.execute(UPDATE_CUSTOMER_WITH_STRIPE_ID, (customer.name, customer.email, customer.id))
        conn.commit()

    # Update last checked time
    new_last_checked = int(time.time())
    cursor.execute(UPDATE_SETTING, (str(new_last_checked),))
    conn.commit()

    cursor.close()
    conn.close()


# Schedule the polling function to run every 10 seconds
schedule.every(10).seconds.do(poll_stripe_customers)

while True:
    schedule.run_pending()
    time.sleep(1)
