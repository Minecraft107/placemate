from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

# ---------------- REGISTER ----------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # FIX: prevent crash if JSON is empty
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    # Validate required fields
    if not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Hash password
    password_hash = bcrypt.hashpw(
        data['password'].encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Create user
    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'id': user.id
    }), 201


# ---------------- LOGIN ----------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # FIX: prevent crash if missing fields
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()

    # Validate user & password
    if not user or not bcrypt.checkpw(
        data['password'].encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        return jsonify({'error': 'Invalid credentials'}), 401

    # JWT identity must be string
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    }), 200


# ---------------- GET CURRENT USER ----------------
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()

    # FIX: safe conversion
    try:
        user = User.query.get(int(user_id))
    except:
        return jsonify({'error': 'Invalid user ID in token'}), 400

    # FIX: user exists check
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email
    }), 200