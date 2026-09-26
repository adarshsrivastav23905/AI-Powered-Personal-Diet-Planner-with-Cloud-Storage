"""
Authentication Routes
======================
Handles user registration, login, and logout.

Endpoints:
    POST /api/auth/register - Register a new user
    POST /api/auth/login    - Login and receive JWT token
    POST /api/auth/logout   - Logout (client-side token removal)
    GET  /api/auth/me       - Get current user info from token

Cloud Computing Concepts Demonstrated:
- User Authentication: Secure identity verification
- RESTful API Design: Stateless request handling
- Password Security: Hashed storage, never plain text
"""

import json
from flask import Blueprint, request, jsonify
from models.database import get_db
from utils.auth_helpers import (
    hash_password, generate_token, generate_user_id, token_required
)
from utils.validators import validate_email, validate_password, sanitize_string

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request Body:
        {
            "name": "Demo User",
            "email": "demo@example.com",
            "password": "demo123"
        }
    
    Returns:
        201: User created successfully with JWT token
        400: Validation error
        409: Email already exists
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    # Extract and sanitize fields
    name = sanitize_string(data.get('name', ''))
    email = sanitize_string(data.get('email', '')).lower()
    password = data.get('password', '')

    # Validate inputs
    if not name or len(name) < 2:
        return jsonify({'error': 'Name must be at least 2 characters'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return jsonify({'error': error_msg}), 400

    # Check if email already exists
    db = get_db()
    existing = db.execute('SELECT user_id FROM users WHERE email = ?', (email,)).fetchone()
    if existing:
        db.close()
        return jsonify({'error': 'An account with this email already exists'}), 409

    # Create user
    user_id = generate_user_id()
    password_hash = hash_password(password)

    db.execute(
        '''INSERT INTO users (user_id, name, email, password_hash)
           VALUES (?, ?, ?, ?)''',
        (user_id, name, email, password_hash)
    )
    db.commit()
    db.close()

    # Generate JWT token
    token = generate_token(user_id, email)

    return jsonify({
        'message': 'Registration successful',
        'token': token,
        'user': {
            'user_id': user_id,
            'name': name,
            'email': email,
            'profile_completed': False
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    
    Request Body:
        {
            "email": "demo@example.com",
            "password": "demo123"
        }
    
    Returns:
        200: Login successful with JWT token
        400: Missing fields
        401: Invalid credentials
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    email = sanitize_string(data.get('email', '')).lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Find user
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE email = ?', (email,)
    ).fetchone()
    db.close()

    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    # Verify password
    if user['password_hash'] != hash_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Generate JWT token
    token = generate_token(user['user_id'], email)

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'user_id': user['user_id'],
            'name': user['name'],
            'email': user['email'],
            'profile_completed': bool(user['profile_completed'])
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout endpoint.
    Since JWT is stateless, actual token invalidation happens client-side.
    This endpoint exists for API completeness and logging.
    
    Returns:
        200: Logout acknowledged
    """
    return jsonify({'message': 'Logout successful. Please remove token from client.'}), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id):
    """
    Get current authenticated user's basic info.
    Protected route - requires valid JWT token.
    
    Returns:
        200: User info
        404: User not found
    """
    db = get_db()
    user = db.execute(
        'SELECT user_id, name, email, profile_completed FROM users WHERE user_id = ?',
        (user_id,)
    ).fetchone()
    db.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user': {
            'user_id': user['user_id'],
            'name': user['name'],
            'email': user['email'],
            'profile_completed': bool(user['profile_completed'])
        }
    }), 200
