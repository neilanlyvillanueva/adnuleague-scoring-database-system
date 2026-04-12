from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

# Default credentials - change these as needed
DEFAULT_USERS = {
    'admin': {
        'password': 'admin123',
        'role': 'admin'
    },
    'tabulation': {
        'password': 'tabulation123',
        'role': 'tabulation'
    }
}

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
    if role not in ['admin', 'tabulation']:
        return jsonify({'error': 'Invalid role. Must be "admin" or "tabulation"'}), 400

    # Check credentials against default users
    if username not in DEFAULT_USERS:
        return jsonify({'error': 'Invalid credentials'}), 401

    user = DEFAULT_USERS[username]

    if user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    if user['role'] != role:
        return jsonify({'error': f'Invalid role. {username} is not registered as {role}'}), 403

    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': username,
            'username': username,
            'role': user['role']
        }
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    # Registration disabled - credentials are pre-configured
    return jsonify({'error': 'Registration disabled. Contact administrator for credentials.'}), 403

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Client-side should remove the token
    return jsonify({'message': 'Logout successful'}), 200
