from flask import Flask
from routes import register_routes
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://postgres:password@localhost:5000/adnu_intramurals')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register routes
register_routes(app)

@app.route('/')
def index():
    return {'message': 'ADNU League Intramurals Scoring System API'}

if __name__ == '__main__':
    app.run(debug=True)
