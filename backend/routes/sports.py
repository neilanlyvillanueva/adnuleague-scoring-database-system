from flask import Blueprint, request, jsonify
from models import db, Sport, SportCriteria

sports_bp = Blueprint('sports', __name__, url_prefix='/api/sports')

# Mapping between frontend scoringSystemId (1-8) and backend scoring_type (A-H)
SCORING_TYPE_MAP = {
    1: 'A',  # Timed Incremental (1v1)
    2: 'B',  # Ranked Incremental (1v1)
    3: 'C',  # Ranked Incremental (FFA)
    4: 'D',  # Threshold Incremental (1v1)
    5: 'E',  # Ranked Timed (FFA)
    6: 'F',  # Criteria Based (FFA)
    7: 'G',  # Judge Based (FFA)
    8: 'H'   # Win/Lose (FFA)
}

REVERSE_SCORING_TYPE_MAP = {v: k for k, v in SCORING_TYPE_MAP.items()}


# ─── GET all sports ──────────────────────────────────────
@sports_bp.route('', methods=['GET'])
def get_sports():
    """Returns list in the exact shape of state.events in useStore."""
    sports = Sport.query.order_by(Sport.sport_id).all()
    return jsonify([s.to_dict() for s in sports]), 200


# ─── GET single sport ────────────────────────────────────
@sports_bp.route('/<int:sport_id>', methods=['GET'])
def get_sport(sport_id):
    sport = Sport.query.get_or_404(sport_id)
    return jsonify(sport.to_dict()), 200


# ─── POST create sport ───────────────────────────────────
@sports_bp.route('', methods=['POST'])
def create_sport():
    """
    Accepts frontend useStore event shape:
    {
      name, scoringSystemId (1-8), matchupSystem ('1v1'|'FFA'),
      sets (int|null), criteria [{ name, points }]
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = (data.get('name') or '').strip()
    scoring_system_id = data.get('scoringSystemId')
    matchup = data.get('matchupSystem', '1v1')
    category = data.get('category', 'Sports')
    sets = data.get('sets')
    criteria_list = data.get('criteria', [])

    if not name:
        return jsonify({'error': 'name is required'}), 400
    if not scoring_system_id:
        return jsonify({'error': 'scoringSystemId is required'}), 400

    # Convert frontend scoringSystemId (1-8) to backend scoring_type (A-H)
    scoring_type = SCORING_TYPE_MAP.get(int(scoring_system_id))
    if not scoring_type:
        return jsonify({'error': 'Invalid scoringSystemId. Must be 1-8'}), 400

    # Normalize matchup type
    if matchup == 'free-for-all':
        matchup = 'FFA'

    sport = Sport(
        sport_name=name,
        sport_category=category,
        scoring_type=scoring_type,
        matchup_type=matchup,
        is_lower_better=data.get('isLowerBetter', False),
        total_sets_required=int(sets) if sets else 1
    )
    db.session.add(sport)
    db.session.flush()

    for c in criteria_list:
        db.session.add(SportCriteria(
            sport_id=sport.sport_id,
            criteria_name=c.get('name'),
            max_points=c.get('points')
        ))

    db.session.commit()
    return jsonify(sport.to_dict()), 201


# ─── PUT update sport ────────────────────────────────────
@sports_bp.route('/<int:sport_id>', methods=['PUT'])
def update_sport(sport_id):
    """Accepts same shape as POST."""
    sport = Sport.query.get_or_404(sport_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        sport.sport_name = data['name'].strip()
    if 'category' in data:
        sport.sport_category = data['category'].strip()
    if 'scoringSystemId' in data:
        scoring_type = SCORING_TYPE_MAP.get(int(data['scoringSystemId']))
        if scoring_type:
            sport.scoring_type = scoring_type
    if 'matchupSystem' in data:
        matchup = data['matchupSystem']
        sport.matchup_type = 'FFA' if matchup == 'free-for-all' else matchup
    if 'isLowerBetter' in data:
        sport.is_lower_better = data['isLowerBetter']
    if 'sets' in data:
        sport.total_sets_required = int(data['sets']) if data['sets'] else 1

    if 'criteria' in data:
        SportCriteria.query.filter_by(sport_id=sport_id).delete()
        for c in data['criteria']:
            db.session.add(SportCriteria(
                sport_id=sport_id,
                criteria_name=c.get('name'),
                max_points=c.get('points')
            ))

    db.session.commit()
    db.session.refresh(sport)
    return jsonify(sport.to_dict()), 200


# ─── DELETE sport ────────────────────────────────────────
@sports_bp.route('/<int:sport_id>', methods=['DELETE'])
def delete_sport(sport_id):
    sport = Sport.query.get_or_404(sport_id)
    db.session.delete(sport)
    db.session.commit()
    return jsonify({'message': f'Sport {sport_id} deleted'}), 200
