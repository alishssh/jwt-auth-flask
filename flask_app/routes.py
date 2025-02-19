from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_app.models import User, Product
from flask_app import db, bcrypt
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__)    
product_bp = Blueprint('product_bp', __name__)

# ✅ Fetch Users (for testing)
@auth_bp.route("/test-users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        return jsonify({"users": user_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        with current_app.app_context():  
            user = User.query.filter_by(username=data['username']).first()

        if user and bcrypt.check_password_hash(user.hashed_password, data['password']):
            # ✅ Fix: Convert `identity` to a string & use `additional_claims` for role
            access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
            return jsonify({"message": "Login successful!", "access_token": access_token})
        
        return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")  
        return jsonify({"error": str(e)}), 500

# ✅ Admin Authorization Decorator
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        try:
            role = get_jwt().get("role")  # Extract role from JWT claims
            if role != "admin":
                return jsonify({"message": "Admin access required"}), 403
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper

# ✅ Fetch Products (User & Admin)
@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        products = Product.query.all()
        return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/products', methods=['POST'])
@admin_required
def add_product():
    try:
        data = request.get_json()
        if not data or "name" not in data or "price" not in data:
            return jsonify({"message": "Product name and price are required"}), 400
        
        new_product = Product(name=data['name'], price=data['price'])  # ✅ No manual 'id'
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({"message": "Product added successfully!", "product_id": new_product.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Update Product (Admin Only)
@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    try:
        data = request.get_json()
        product = Product.query.get_or_404(product_id)
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        db.session.commit()

        return jsonify({"message": "Product updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Delete Product (Admin Only)
@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Default Route
@auth_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask API!"}), 200
