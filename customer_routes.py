from flask import Blueprint, request, jsonify
from models import Customer, CustomerAccount
from database import db

customer_bp = Blueprint('customers', __name__)

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

@customer_bp.route('/customers/<int:id>', methods=['GET'])
def read_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number})

@customer_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone_number = data.get('phone_number', customer.phone_number)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@customer_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})