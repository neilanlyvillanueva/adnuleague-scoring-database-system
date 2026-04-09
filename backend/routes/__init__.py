from flask import Blueprint

# Import route blueprints
from .auth import auth_bp
from .api import api_bp

def register_routes(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
