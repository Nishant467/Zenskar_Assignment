# services.py
import stripe
from config import Config
from database import create_connection
from flask import jsonify
stripe.api_key = Config.STRIPE_API_KEY

def add_customer(name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
    customer_id = cursor.lastrowid
    conn.commit()
    stripe_customer = stripe.Customer.create(name=name, email=email)
    cursor.execute("UPDATE customers SET stripe_customer_id = ? WHERE id = ?", (stripe_customer.id, customer_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Customer added", "id": customer_id}), 201

def get_customer(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM customers WHERE ID = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"username": user[0], "email": user[1]}), 200
    else:
        return jsonify({"error": "User not found"}), 404

def get_all_customers():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    users = cursor.fetchall()
    conn.close()
    return jsonify({"customers": users}), 200

def update_customer(customer_id, name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, email = ? WHERE id = ?", (name, email, customer_id))
    conn.commit()
    stripe_customer_id = cursor.execute("SELECT stripe_customer_id FROM customers WHERE id = ?", (customer_id,)).fetchone()[0]
    stripe.Customer.modify(stripe_customer_id, name=name, email=email)
    conn.close()
    return jsonify({"message": "Customer updated"}), 200
