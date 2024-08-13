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