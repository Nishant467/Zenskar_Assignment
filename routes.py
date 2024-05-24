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
