# services.py
import stripe
from config import Config
from connection import create_connection
from flask import jsonify
from queries import *
from config import Config
stripe.api_key = Config.STRIPE_API_KEY

def add_customer(name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(ADD_CUSTOMER, (name, email))
    customer_id = cursor.lastrowid
    conn.commit()
    stripe_customer = stripe.Customer.create(name=name, email=email)
    print(stripe_customer)
    cursor.execute(SET_CUSTOMER_STRIPE_ID, (stripe_customer.id, customer_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Customer added", "stripe_customer_id": stripe_customer.id , "id": customer_id}), 201

def get_customer(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(GET_CUSTOMER_FROM_ID, (user_id,))
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
    cursor.execute(UDPATE_CUSTOMER, (name, email, customer_id))
    conn.commit()
    stripe_customer_id = cursor.execute(GET_CUSTOMER_FROM_STRIPE_ID, (customer_id,)).fetchone()[0]
    stripe.Customer.modify(stripe_customer_id, name=name, email=email)
    conn.close()
    return jsonify({"message": "Customer updated"}), 200
