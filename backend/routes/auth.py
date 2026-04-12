from flask import Blueprint, request, jsonify
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')
    role = data.get('role', '')

    # Validation
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    if not role:
        return jsonify({'error': 'Role is required'}), 400
    if role not in ['admin', 'tabulation', 'scorer']:
        return jsonify({'error': 'Invalid role. Must be "admin" or "tabulation"'}), 400

    # Find user in database
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Check password
    if not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Normalize role for comparison (tabulation == scorer)
    user_role = user.role
    requested_role = 'scorer' if role == 'tabulation' else role

    if user_role != requested_role:
        return jsonify({'error': f'Invalid role. {username} is not registered as {role}'}), 403

    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.user_id,
            'username': user.username,
            'role': user.role
        }
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    # Registration disabled - contact administrator
    return jsonify({'error': 'Registration disabled. Contact administrator for credentials.'}), 403

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Client-side should remove the token
    return jsonify({'message': 'Logout successful'}), 200
