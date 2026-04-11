from flask import Blueprint, jsonify
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required # ADD THIS BACK

api_bp = Blueprint('api', __name__)

@api_bp.route('/scores', methods=['GET'])
@jwt_required()
def get_scores():
    return jsonify({"scores": "League data here"})

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@api_bp.route('/teams', methods=['GET'])
@jwt_required()
def get_teams():
    return jsonify({'message': 'endpoint'}), 200

@api_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():

    return jsonify({'message': 'endpoint'}), 200
