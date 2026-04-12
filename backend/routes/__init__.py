from flask import Blueprint

# Import route blueprints
from .auth import auth_bp
from .api import api_bp
from .sports import sports_bp
from .teams import teams_bp
from .games import games_bp
from .leaderboard import leaderboard_bp

def register_routes(app):
    """Register all blueprints with the Flask app

    Note: Blueprints with url_prefix in their definition don't need additional prefix here.
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    # These blueprints have their own url_prefix defined in their files
    app.register_blueprint(sports_bp)  # /api/sports
    app.register_blueprint(teams_bp)   # /api/teams
    app.register_blueprint(games_bp)   # /api/games
    app.register_blueprint(leaderboard_bp)  # /api/leaderboard
