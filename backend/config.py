import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database - SQLite by default for development, switch to PostgreSQL when ready
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')  # 'sqlite' or 'postgresql'

    if DATABASE_TYPE == 'postgresql':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:password@localhost:5432/adnu_intramurals')
    else:
        # Use absolute path for SQLite database
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'instance', 'adnu_intramurals.db'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
