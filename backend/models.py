from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# 1. Sport Table
class Sport(db.Model):
    __tablename__ = 'sport'

    sport_id = Column(Integer, primary_key=True)
    sport_name = Column(String(100), nullable=False)
    sport_category = Column(String(100), default='Sports')
    scoring_system_id = Column(Integer, nullable=False)
    matchup_type = Column(String(20), nullable=False)  # '1v1' or 'free-for-all'
    is_lower_better = Column(Boolean, default=False)
    total_sets_required = Column(Integer, default=1)

    criteria = db.relationship('SportCriteria', backref='sport', cascade='all, delete-orphan', lazy=True)
    team_participations = db.relationship('TeamParticipation', backref='sport', cascade='all, delete-orphan', lazy=True)
    games = db.relationship('Game', backref='sport', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.sport_id,
            'name': self.sport_name,
            'category': self.sport_category,
            'scoringSystemId': self.scoring_system_id,
            'matchupSystem': self.matchup_type,
            'sets': self.total_sets_required if self.total_sets_required else None,
            'criteria': [{'name': c.criteria_name, 'points': c.max_points} for c in self.criteria]
        }


# 2. Criteria/Judge Table
class SportCriteria(db.Model):
    __tablename__ = 'sport_criteria'

    criteria_id = Column(Integer, primary_key=True)
    sport_id = Column(Integer, ForeignKey('sport.sport_id', ondelete='CASCADE'), nullable=False)
    criteria_name = Column(String(100))
    max_points = Column(Integer)


# 3. Team Table (Identity Only)
class Team(db.Model):
    __tablename__ = 'team'

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String(100), unique=True, nullable=False)
    team_color = Column(String(20), default='#0038A8')

    participations = db.relationship('TeamParticipation', backref='team', cascade='all, delete-orphan', lazy=True)
    game_results = db.relationship('GameResult', backref='team', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.team_id,
            'name': self.team_name,
            'color': self.team_color,
            'participatingSports': [p.sport_id for p in self.participations]
        }


# 4. Participation Table (MANY-TO-MANY)
class TeamParticipation(db.Model):
    __tablename__ = 'team_participation'
    __table_args__ = (UniqueConstraint('team_id', 'sport_id'),)

    participation_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id', ondelete='CASCADE'), nullable=False)
    sport_id = Column(Integer, ForeignKey('sport.sport_id', ondelete='CASCADE'), nullable=False)


# 5. User Table (For Authorization)
class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), default='scorer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# 6. Game Table
class Game(db.Model):
    __tablename__ = 'game'

    game_id = Column(Integer, primary_key=True)
    sport_id = Column(Integer, ForeignKey('sport.sport_id'), nullable=False)
    venue = Column(String(100))
    school_year = Column(String(15), nullable=False)
    season = Column(String(20), nullable=False)
    game_status = Column(String(20), default='Upcoming')

    results = db.relationship('GameResult', backref='game', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.game_id,
            'sportId': self.sport_id,
            'venue': self.venue,
            'schoolYear': self.school_year,
            'season': self.season,
            'status': self.game_status,
            'results': [
                {
                    'teamId': r.team_id,
                    'finalScore': float(r.final_score) if r.final_score else 0,
                    'isWinner': r.is_winner
                }
                for r in self.results
            ]
        }


# 7. Game Result
class GameResult(db.Model):
    __tablename__ = 'game_result'

    result_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.game_id', ondelete='CASCADE'), nullable=False)
    team_id = Column(Integer, ForeignKey('team.team_id'), nullable=False)
    final_score = Column(Numeric(10, 3))
    is_winner = Column(Boolean, default=False)

    score_breakdown = db.relationship('ScoreBreakdown', backref='result', cascade='all, delete-orphan', lazy=True)


# 8. Score Breakdown
class ScoreBreakdown(db.Model):
    __tablename__ = 'score_breakdown'

    breakdown_id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey('game_result.result_id', ondelete='CASCADE'), nullable=False)
    component_name = Column(String(100))
    points_awarded = Column(Numeric(10, 2))
