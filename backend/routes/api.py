from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

# HEALTH CHECK
@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200
