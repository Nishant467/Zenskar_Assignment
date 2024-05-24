from flask import request, jsonify
import stripe
import sqlite3
from services import get_customer, get_all_customers, add_customer, update_customer 
from config import Config
stripe.api_key = Config.STRIPE_API_KEY

def get_user_route(user_id):
    return get_customer(user_id)

def get_users_route():
    return get_all_customers()

def add_customer_route():
    data = request.get_json()
    return add_customer(data['name'], data['email'])

def update_customer_route():
    data = request.get_json()
    return update_customer(data['id'], data['name'], data['email'])

def handle_webhook():
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    payload = request.get_json()
    event = None

    try:
        event = stripe.Event.construct_from(
            payload, stripe.api_key
        )
    except ValueError as e:
        return jsonify(error=str(e)), 400

    data = event.data.object

    if event.type == "customer.created":
        add_customer(data['name'], data['email'])
    elif event.type == "customer.updated":
        update_customer(data['id'], data['name'], data['email'])

    return jsonify(success=True), 200