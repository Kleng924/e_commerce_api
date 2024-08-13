pip install Flask Flask-SQLAlchemy

#Database Configuration:

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/ecommerce_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Deine Models:

from database import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Pending')

#Implement CRUD operations:

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

#Product Routes:

from flask import Blueprint, request, jsonify
from models import Product
from database import db

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], stock=data.get('stock', 0))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@product_bp.route('/products/<int:id>', methods=['GET'])
def read_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'stock': product.stock})

@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

@product_bp.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'price': product.price, 'stock': product.stock} for product in products])

#Order Routes:

from flask import Blueprint, request, jsonify
from models import Order, Product
from database import db
from datetime import datetime

order_bp = Blueprint('orders', __name__)

@order_bp.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(customer_id=data['customer_id'], order_date=datetime.utcnow(), status='Pending')
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'}), 201

@order_bp.route('/orders/<int:id>', methods=['GET'])
def retrieve_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({'id': order.id, 'customer_id': order.customer_id, 'order_date': order.order_date, 'status': order.status})

@order_bp.route('/orders/<int:id>/track', methods=['GET'])
def track_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({'id': order.id, 'status': order.status, 'expected_delivery': 'TBD'})

@order_bp.route('/orders/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    order = Order.query.get_or_404(id)
    if order.status != 'Shipped':
        order.status = 'Canceled'
        db.session.commit()
        return jsonify({'message': 'Order canceled successfully'})
    else:
        return jsonify({'message': 'Cannot cancel a shipped order'}), 400

#Integrate Routes in app.py:

from flask import Flask
from customer_routes import customer_bp
from product_routes import product_bp
from order_routes import order_bp
from database import db, app

app.register_blueprint(customer_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

