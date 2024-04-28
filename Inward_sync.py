import stripe
import schedule
import time
import sqlite3

# Initialize Stripe API
stripe.api_key = 'sk_test_51P8z4XSElIyrQVH2QnPsaVc17uN7hmMzTDzQd7VA7ij7ROAVsyFXAum3IrxrvD27l6G3ThvPjTD7ugicTtvZ2KIM00UNGZAKzT'

def poll_stripe_customers():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Get the last checked time from your database
    cursor.execute("SELECT value FROM settings WHERE key = 'last_checked'")
    last_checked = cursor.fetchone()[0]

    # Assuming last_checked is stored as a Unix timestamp
    # Fetch recent customers from Stripe
    customers = stripe.Customer.list(created={'gte': last_checked})
    for customer in customers.auto_paging_iter():
        print(customer)
        # Update local database with new info
        cursor.execute("""
            UPDATE customers
            SET name = ?, email = ?
            WHERE stripe_customer_id = ?
        """, (customer.name, customer.email, customer.id))
        conn.commit()

    # Update last checked time
    new_last_checked = int(time.time())
    cursor.execute("UPDATE settings SET value = ? WHERE key = 'last_checked'", (str(new_last_checked),))
    conn.commit()

    cursor.close()
    conn.close()


# Schedule the polling function to run every 10 seconds
schedule.every(10).seconds.do(poll_stripe_customers)

while True:
    schedule.run_pending()
    time.sleep(1)
