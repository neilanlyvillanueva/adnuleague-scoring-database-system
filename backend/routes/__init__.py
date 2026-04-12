from flask import Blueprint

# Import route blueprints
from .auth import auth_bp
from .api import api_bp
from .sports import sports_bp
from .teams import teams_bp
from .games import games_bp
from .leaderboard import leaderboard_bp

def register_routes(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(sports_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(leaderboard_bp)
