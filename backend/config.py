import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')

    if DATABASE_TYPE == 'postgresql':
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOST = os.getenv('DB_HOST')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_NAME = os.getenv('DB_NAME', 'postgres')

        from urllib.parse import quote_plus
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'adnu_intramurals.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')