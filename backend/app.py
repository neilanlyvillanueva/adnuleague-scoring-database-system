from flask import Flask
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

    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register all route blueprints
    register_routes(app)

    @app.route('/')
    def index():
        return {'message': 'ADNU League Intramurals Scoring System API'}

    # Create all tables and seed default users on first run
    with app.app_context():
        db.create_all()
        _seed_default_users()

    return app


def _seed_default_users():
    """Create default admin and scorer users if they don't exist."""
    from models import User
    defaults = [
        {'username': 'admin',       'password': 'admin123',       'role': 'admin'},
        {'username': 'tabulation',  'password': 'tabulation123',  'role': 'scorer'},
    ]
    for u in defaults:
        if not User.query.filter_by(username=u['username']).first():
            user = User(username=u['username'], role=u['role'])
            user.set_password(u['password'])
            db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
