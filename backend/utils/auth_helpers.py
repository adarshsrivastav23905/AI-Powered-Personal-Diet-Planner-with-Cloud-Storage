"""
Authentication Helpers
=======================
JWT token generation and verification utilities.

Cloud Computing Concept Demonstrated:
- Authentication: Verifying user identity with JWT tokens
- Authorization: Ensuring users can only access their own resources
- Security: Password hashing, token expiration, secure headers
"""

import os
import jwt
import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify


# Secret key for JWT signing
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-jwt-secret-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with a salt.
    In production, use bcrypt or argon2 for stronger security.
    """
    salt = os.getenv('PASSWORD_SALT', 'diet-planner-salt')
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def generate_token(user_id: str, email: str) -> str:
    """Generate a JWT token for an authenticated user."""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """
    Decorator to protect routes that require authentication.
    Extracts user_id from the JWT token in the Authorization header.
    
    Cloud Computing Concept: Authorization middleware
    - Ensures only authenticated users can access protected endpoints
    - Extracts user identity for data isolation
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Authentication token is required'}), 401

        # Decode and verify token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Pass user_id to the route handler
        return f(payload['user_id'], *args, **kwargs)

    return decorated


def generate_user_id() -> str:
    """Generate a unique user ID."""
    return str(uuid.uuid4())


def generate_plan_id() -> str:
    """Generate a unique plan ID."""
    return f"plan_{uuid.uuid4().hex[:12]}"


def generate_file_id() -> str:
    """Generate a unique file ID."""
    return f"file_{uuid.uuid4().hex[:12]}"
