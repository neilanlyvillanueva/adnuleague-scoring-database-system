from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

# HEALTH CHECK
api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@api_bp.route('/events', methods=['GET'])
def get_events():
    return jsonify({'message': 'endpoint'}), 200

@api_bp.route('/teams', methods=['GET'])
def get_teams():
    return jsonify({'message': 'endpoint'}), 200

@api_bp.route('/scores', methods=['GET'])
def get_scores():
    return jsonify({"scores": "League data here"})

@api_bp.route('/matches', methods=['GET'])
def get_matches():
    return jsonify({'message': 'endpoint'}), 200
