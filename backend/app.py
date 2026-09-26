"""
AI-Powered Personal Diet Planner - Main Application
=====================================================
Cloud Computing Course Project
This is the main entry point for the Flask backend server.
It registers all route blueprints and configures the application.

DISCLAIMER: Generated diet plans are for educational/general wellness
demonstration only and do NOT constitute medical or clinical nutrition advice.
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import route blueprints
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.plan_routes import plan_bp
from routes.storage_routes import storage_bp

# Import database initialization
from models.database import init_db


def create_app():
    """Application factory pattern for creating the Flask app."""
    app = Flask(__name__)

    # ── Configuration ──────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

    # ── CORS ───────────────────────────────────────────────────────
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # ── Ensure upload directory exists ─────────────────────────────
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # ── Initialize Database ────────────────────────────────────────
    init_db()

    # ── Register Blueprints ────────────────────────────────────────
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(plan_bp, url_prefix='/api/plans')
    app.register_blueprint(storage_bp, url_prefix='/api/storage')

    # ── Health Check Endpoint ──────────────────────────────────────
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring and deployment verification."""
        return {"status": "healthy", "service": "AI Diet Planner API", "version": "1.0.0"}, 200

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    print(f"\n🥗 AI Diet Planner API running on http://localhost:{port}")
    print(f"📋 Health check: http://localhost:{port}/api/health\n")
    app.run(host='0.0.0.0', port=port, debug=debug)
