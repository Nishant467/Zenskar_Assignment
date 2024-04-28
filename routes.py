# routes.py
from flask import request,jsonify
from services import add_customer, get_customer, get_all_customers, update_customer

def initialize_routes(app):
    @app.route('/get_customer/<int:user_id>', methods=['GET'])
    def get_user_route(user_id):
        return get_customer(user_id)

    @app.route('/get_customers', methods=['GET'])
    def get_users_route():
        return get_all_customers()

    @app.route('/add_customer', methods=['POST'])
    def add_customer_route():
        data = request.get_json()
        return add_customer(data['name'], data['email'])

    @app.route('/update_customer', methods=['POST'])
    def update_customer_route():
        data = request.get_json()
        return update_customer(data['id'], data['name'], data['email'])
