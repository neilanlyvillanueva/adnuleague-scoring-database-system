from flask import Flask
from flask_cors import CORS
from config import Config
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register routes
    register_routes(app)

    @app.route('/')
    def index():
        return {'message': 'ADNU League Intramurals Scoring System API'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
