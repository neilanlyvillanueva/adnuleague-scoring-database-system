from flask import Blueprint, jsonify
from models import db
from sqlalchemy import text

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/api/leaderboard')


# ─── GET overall leaderboard ─────────────────────────────
@leaderboard_bp.route('', methods=['GET'])
def get_leaderboard():
    """
    Returns data matching getLeaderboard() output from useStore:
    [{ teamId, teamName, teamColor, wins, gamesPlayed, overallPoints }]
    """
    rows = db.session.execute(text("""
        SELECT team_id, team_name, team_color, total_wins, games_played, overall_points
        FROM overall_leaderboard
    """)).mappings().all()

    return jsonify([
        {
            'teamId':        row['team_id'],
            'teamName':      row['team_name'],
            'teamColor':     row['team_color'],
            'wins':          row['total_wins'],
            'gamesPlayed':   row['games_played'],
            'overallPoints': row['overall_points']
        }
        for row in rows
    ]), 200


# ─── GET match history ───────────────────────────────────
@leaderboard_bp.route('/history', methods=['GET'])
def get_history():
    """
    Returns match history from the DB view.
    participants[] entries match game_result rows.
    """
    rows = db.session.execute(text("""
        SELECT game_id, sport_id, sport_name, sport_category, matchup_type,
               venue, game_status, school_year, season, participants
        FROM match_history_view
    """)).mappings().all()

    return jsonify([
        {
            'gameId':      row['game_id'],
            'sportId':     row['sport_id'],
            'sportName':   row['sport_name'],
            'category':    row['sport_category'],
            'matchupType': row['matchup_type'],
            'venue':       row['venue'],
            'status':      row['game_status'],
            'schoolYear':  row['school_year'],
            'season':      row['season'],
            'participants': row['participants']
        }
        for row in rows
    ]), 200
