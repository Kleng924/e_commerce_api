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