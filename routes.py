# routes.py
from flask import request,jsonify
from services import add_customer, get_customer, get_all_customers, update_customer
import stripe, sqlite3
stripe.api_key = 'sk_test_51P8z4XSElIyrQVH2QnPsaVc17uN7hmMzTDzQd7VA7ij7ROAVsyFXAum3IrxrvD27l6G3ThvPjTD7ugicTtvZ2KIM00UNGZAKzT'

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

    @app.route('/stripe/webhook', methods=['POST'])
    def handle_webhook():
        conn = sqlite3.connect('mydatabase.db')
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
        # Handle the event
        # if event.type == 'customer.created' or event.type == 'customer.updated':
        #     customer_data = event.data.object
        #     cursor.execute("""
        #     UPDATE customers
        #     SET name = ?, email = ?
        #     WHERE stripe_customer_id = ?
        # """, (customer_data.name, customer_data.email, customer_data.id))
        # conn.commit()
        # conn.close()

        if event.type == "customer.created":
            add_customer(data['name'], data['email'])
        elif event.type == "customer.updated":
            update_customer(data['id'], data['name'], data['email'])

        return jsonify(success=True), 200
