from flask import Blueprint, request, jsonify
from models import db, Game, GameResult, ScoreBreakdown, Sport, Team

games_bp = Blueprint('games', __name__, url_prefix='/api/games')


# ─── GET all games ───────────────────────────────────────
@games_bp.route('', methods=['GET'])
def get_games():
    """Returns list in the exact shape of state.matches in useStore."""
    games = Game.query.order_by(Game.game_id.desc()).all()
    return jsonify([g.to_dict() for g in games]), 200


# ─── GET single game ─────────────────────────────────────
@games_bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify(game.to_dict()), 200


# ─── POST create game ────────────────────────────────────
@games_bp.route('', methods=['POST'])
def create_game():
    """
    Accepts frontend match creation shape:
    {
      eventId:      int,            -- sport_id
      matchupType:  '1v1' | 'free-for-all',
      teamAId:      int | null,     -- for 1v1
      teamBId:      int | null,     -- for 1v1
      participants: [int, ...],     -- for FFA
      venue:        str
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    event_id    = data.get('eventId')
    matchup     = data.get('matchupType', '1v1')
    venue       = (data.get('venue') or '').strip()
    team_a_id   = data.get('teamAId')
    team_b_id   = data.get('teamBId')
    participants = data.get('participants', [])

    if not event_id:
        return jsonify({'error': 'eventId is required'}), 400
    if not venue:
        return jsonify({'error': 'venue is required'}), 400

    Sport.query.get_or_404(event_id)

    if matchup == '1v1':
        if not team_a_id or not team_b_id:
            return jsonify({'error': 'teamAId and teamBId are required for 1v1'}), 400
        if team_a_id == team_b_id:
            return jsonify({'error': 'Teams must be different'}), 400
        participant_ids = [team_a_id, team_b_id]
    else:
        if len(participants) < 2:
            return jsonify({'error': 'At least 2 participants required for FFA'}), 400
        participant_ids = participants

    game = Game(
        sport_id    = event_id,
        venue       = venue,
        school_year = data.get('schoolYear', '2024-2025'),
        season      = data.get('season', 'Intramurals'),
        game_status = 'ongoing'
    )
    db.session.add(game)
    db.session.flush()

    for team_id in participant_ids:
        Team.query.get_or_404(team_id)
        db.session.add(GameResult(
            game_id     = game.game_id,
            team_id     = team_id,
            final_score = 0,
            is_winner   = False
        ))

    db.session.commit()
    db.session.refresh(game)
    return jsonify(game.to_dict()), 201


# ─── DELETE game ─────────────────────────────────────────
@games_bp.route('/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': f'Game {game_id} deleted'}), 200


# ─── POST finalize game ──────────────────────────────────
@games_bp.route('/<int:game_id>/finalize', methods=['POST'])
def finalize_game(game_id):
    """
    Accepts the same data that finalizeMatch() writes in useStore:
    {
      scores:    { teamA: num, teamB: num }    -- for 1v1
                 { <teamId>: num, ... }        -- for FFA (key is team_id as string or int)
      setScores: [{ set: 1, teamA: num, teamB: num }, ...]  -- optional, for scoringSystemId=4
      winner:    <teamId> | null,
      status:    'completed'
    }
    """
    game = Game.query.get_or_404(game_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    scores      = data.get('scores', {})
    set_scores  = data.get('setScores', [])
    winner_id   = data.get('winner')
    results     = game.results
    matchup     = game.sport.matchup_type if game.sport else '1v1'

    if matchup == '1v1' and len(results) >= 2:
        team_a_result = results[0]
        team_b_result = results[1]

        team_a_result.final_score = scores.get('teamA', 0)
        team_b_result.final_score = scores.get('teamB', 0)
        team_a_result.is_winner = (team_a_result.team_id == winner_id)
        team_b_result.is_winner = (team_b_result.team_id == winner_id)

        # Persist set scores as score_breakdown rows (component_name = 'set_N')
        ScoreBreakdown.query.filter_by(result_id=team_a_result.result_id).delete()
        ScoreBreakdown.query.filter_by(result_id=team_b_result.result_id).delete()
        for s in set_scores:
            n = s.get('set', 0)
            db.session.add(ScoreBreakdown(
                result_id      = team_a_result.result_id,
                component_name = f'set_{n}',
                points_awarded = s.get('teamA', 0)
            ))
            db.session.add(ScoreBreakdown(
                result_id      = team_b_result.result_id,
                component_name = f'set_{n}',
                points_awarded = s.get('teamB', 0)
            ))
    else:
        # FFA — scores is { teamId: score }
        for result in results:
            key = str(result.team_id)
            if key in scores:
                result.final_score = scores[key]
            elif result.team_id in scores:
                result.final_score = scores[result.team_id]
            result.is_winner = (result.team_id == winner_id)

    game.game_status = 'completed'
    db.session.commit()
    db.session.refresh(game)
    return jsonify(game.to_dict()), 200
