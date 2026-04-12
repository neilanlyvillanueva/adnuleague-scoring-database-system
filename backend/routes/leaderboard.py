from flask import Blueprint, jsonify
from models import db, Team
from sqlalchemy import text

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/api/leaderboard')


# ─── GET overall leaderboard ─────────────────────────────
@leaderboard_bp.route('', methods=['GET'])
def get_leaderboard():
    """
    Returns leaderboard data from the overall_leaderboard view.
    Schema view returns: team_name, total_wins, games_played, overall_points
    We need to join with team to get team_id for the frontend.
    """
    rows = db.session.execute(text("""
        SELECT
            t.team_id,
            lb.team_name,
            lb.total_wins,
            lb.games_played,
            lb.overall_points
        FROM overall_leaderboard lb
        JOIN team t ON lb.team_name = t.team_name
        ORDER BY lb.overall_points DESC
    """)).mappings().all()

    # Generate consistent colors for frontend
    colors = ['#0038A8', '#FFD700', '#FF4D4D', '#00A859', '#8B5CF6', '#F59E0B', '#EC4899', '#10B981']

    return jsonify([
        {
            'teamId': row['team_id'],
            'teamName': row['team_name'],
            'teamColor': colors[row['team_id'] % len(colors)] if row['team_id'] else '#0038A8',
            'wins': row['total_wins'],
            'gamesPlayed': row['games_played'],
            'overallPoints': row['overall_points']
        }
        for row in rows
    ]), 200


# ─── GET match history ───────────────────────────────────
@leaderboard_bp.route('/history', methods=['GET'])
def get_history():
    """
    Returns match history from the match_history_view.
    Schema view returns: sport_name, game_id, game_status, matchup (string_agg)
    """
    rows = db.session.execute(text("""
        SELECT
            g.game_id,
            s.sport_id,
            s.sport_name,
            s.scoring_type,
            s.matchup_type,
            g.venue,
            g.game_status,
            g.school_year,
            g.season
        FROM game g
        JOIN sport s ON g.sport_id = s.sport_id
        ORDER BY g.game_id DESC
    """)).mappings().all()

    results = []
    for row in rows:
        # Get participants for this game
        participants_rows = db.session.execute(text("""
            SELECT
                t.team_id,
                t.team_name,
                gr.final_score,
                gr.is_winner
            FROM game_result gr
            JOIN team t ON gr.team_id = t.team_id
            WHERE gr.game_id = :game_id
            ORDER BY gr.is_winner DESC, gr.final_score DESC
        """), {'game_id': row['game_id']}).mappings().all()

        participants = [
            {
                'teamId': p['team_id'],
                'teamName': p['team_name'],
                'finalScore': float(p['final_score']) if p['final_score'] else 0,
                'isWinner': p['is_winner']
            }
            for p in participants_rows
        ]

        results.append({
            'gameId': row['game_id'],
            'sportId': row['sport_id'],
            'sportName': row['sport_name'],
            'category': 'Sports',  # Default category since schema doesn't have it
            'matchupType': row['matchup_type'],
            'venue': row['venue'] or 'TBA',
            'status': row['game_status'],
            'schoolYear': row['school_year'],
            'season': row['season'],
            'participants': participants
        })

    return jsonify(results), 200
