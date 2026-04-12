from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from routes import register_routes
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # CORS configuration - allow frontend on localhost:5173
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5173", "http://localhost:5174"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Register all route blueprints
    register_routes(app)

    @app.route('/')
    def index():
        return jsonify({'message': 'ADNU League Intramurals Scoring System API'})

    @app.route('/api/health')
    def health():
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            return jsonify({'status': 'healthy', 'database': 'connected'}), 200
        except Exception as e:
            return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

    # Create all tables and seed default users on first run
    with app.app_context():
        try:
            # Try to create tables (will skip if they exist)
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            _seed_default_users()
        except Exception as e:
            app.logger.error(f"Database initialization error: {e}")

    return app


def _seed_default_users():
    """Create default admin and scorer users if they don't exist."""
    from models import User
    from werkzeug.security import generate_password_hash

    defaults = [
        {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
        {'username': 'tabulation', 'password': 'tabulation123', 'role': 'scorer'},
    ]

    for u in defaults:
        if not User.query.filter_by(username=u['username']).first():
            user = User(username=u['username'], role=u['role'])
            user.set_password(u['password'])
            db.session.add(user)

    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
