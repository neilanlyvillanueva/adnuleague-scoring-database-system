from flask import Blueprint, request, jsonify
from models import db, Team, TeamParticipation, Sport

teams_bp = Blueprint('teams', __name__, url_prefix='/api/teams')


# ─── GET all teams ───────────────────────────────────────
@teams_bp.route('', methods=['GET'])
def get_teams():
    """Returns list in the exact shape of state.teams in useStore:
    [{ id, name, color, participatingSports: [sport_id, ...] }]
    """
    teams = Team.query.order_by(Team.team_id).all()
    return jsonify([t.to_dict() for t in teams]), 200


# ─── GET single team ─────────────────────────────────────
@teams_bp.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = Team.query.get_or_404(team_id)
    return jsonify(team.to_dict()), 200


# ─── POST create team ────────────────────────────────────
@teams_bp.route('', methods=['POST'])
def create_team():
    """
    Accepts: { name, color }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'name is required'}), 400
    if Team.query.filter_by(team_name=name).first():
        return jsonify({'error': 'Team name already exists'}), 409

    team = Team(team_name=name, team_color=data.get('color', '#0038A8'))
    db.session.add(team)
    db.session.commit()
    return jsonify(team.to_dict()), 201


# ─── PUT update team ─────────────────────────────────────
@teams_bp.route('/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    """Accepts: { name?, color? }"""
    team = Team.query.get_or_404(team_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        new_name = data['name'].strip()
        existing = Team.query.filter_by(team_name=new_name).first()
        if existing and existing.team_id != team_id:
            return jsonify({'error': 'Team name already exists'}), 409
        team.team_name = new_name

    if 'color' in data:
        team.team_color = data['color']

    db.session.commit()
    return jsonify(team.to_dict()), 200


# ─── DELETE team ─────────────────────────────────────────
@teams_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': f'Team {team_id} deleted'}), 200


# ─── POST toggle participation ────────────────────────────
@teams_bp.route('/<int:team_id>/participation/<int:sport_id>', methods=['POST'])
def toggle_participation(team_id, sport_id):
    """
    Toggle a team's participation in a sport (same as toggleTeamSportParticipation in useStore).
    Returns: { participating: bool, teamId, sportId, team: <full team dict> }
    """
    Team.query.get_or_404(team_id)
    Sport.query.get_or_404(sport_id)

    existing = TeamParticipation.query.filter_by(
        team_id=team_id, sport_id=sport_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        participating = False
    else:
        db.session.add(TeamParticipation(team_id=team_id, sport_id=sport_id))
        db.session.commit()
        participating = True

    team = Team.query.get(team_id)
    return jsonify({
        'participating': participating,
        'teamId':        team_id,
        'sportId':       sport_id,
        'team':          team.to_dict()
    }), 200
