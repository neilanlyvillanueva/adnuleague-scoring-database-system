from flask import Blueprint, request, jsonify
from models import db, Sport, SportCriteria

sports_bp = Blueprint('sports', __name__, url_prefix='/api/sports')


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
      name, category, scoringSystemId, matchupSystem ('1v1'|'free-for-all'),
      sets (int|null), criteria [{ name, points }]
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = (data.get('name') or '').strip()
    category = data.get('category', 'Sports')
    scoring_system_id = data.get('scoringSystemId')
    matchup = data.get('matchupSystem', '1v1')
    sets = data.get('sets')
    criteria_list = data.get('criteria', [])

    if not name:
        return jsonify({'error': 'name is required'}), 400
    if not scoring_system_id:
        return jsonify({'error': 'scoringSystemId is required'}), 400
    if matchup not in ('1v1', 'free-for-all'):
        return jsonify({'error': 'matchupSystem must be "1v1" or "free-for-all"'}), 400

    sport = Sport(
        sport_name=name,
        sport_category=category,
        scoring_system_id=int(scoring_system_id),
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
        sport.sport_category = data['category']
    if 'scoringSystemId' in data:
        sport.scoring_system_id = int(data['scoringSystemId'])
    if 'matchupSystem' in data:
        sport.matchup_type = data['matchupSystem']
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
