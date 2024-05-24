# routes.py
# from flask import request,jsonify
# from services import add_customer, get_customer, get_all_customers, update_customer
# import stripe, sqlite3
# from config import Config
# stripe.api_key = Config.STRIPE_API_KEY

# def initialize_routes(app):
#     @app.route('/get_customer/<int:user_id>', methods=['GET'])
#     def get_user_route(user_id):
#         return get_customer(user_id)

#     @app.route('/get_customers', methods=['GET'])
#     def get_users_route():
#         return get_all_customers()

#     @app.route('/add_customer', methods=['POST'])
#     def add_customer_route():
#         data = request.get_json()
#         return add_customer(data['name'], data['email'])

#     @app.route('/update_customer', methods=['POST'])
#     def update_customer_route():
#         data = request.get_json()
#         return update_customer(data['id'], data['name'], data['email'])

#     @app.route('/stripe/webhook', methods=['POST'])
#     def handle_webhook():
#         conn = sqlite3.connect(Config.DATABASE)
#         cursor = conn.cursor()
#         payload = request.get_json()
#         event = None

#         try:
#             event = stripe.Event.construct_from(
#                 payload, stripe.api_key
#             )
#         except ValueError as e:
#             return jsonify(error=str(e)), 400

#         data = event.data.object

#         if event.type == "customer.created":
#             add_customer(data['name'], data['email'])
#         elif event.type == "customer.updated":
#             update_customer(data['id'], data['name'], data['email'])

#         return jsonify(success=True), 200

from flask import Flask
from customers_handlers import (
    get_user_route, get_users_route, 
    add_customer_route, update_customer_route, 
    handle_webhook  # Import the webhook handler
)

def initialize_routes(app):
    @app.route('/get_customer/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        return get_user_route(user_id)

    @app.route('/get_customers', methods=['GET'])
    def get_users():
        return get_users_route()

    @app.route('/add_customer', methods=['POST'])
    def add_customer():
        return add_customer_route()

    @app.route('/update_customer', methods=['POST'])
    def update_customer():
        return update_customer_route()

    @app.route('/stripe/webhook', methods=['POST'])
    def webhook():
        return handle_webhook()
