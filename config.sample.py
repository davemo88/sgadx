from os import path
from datetime import timedelta

top_dir = path.abspath(path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(top_dir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = path.join(top_dir, 'db_repository')

PERMANENT_SESSION_LIFETIME = timedelta(minutes=24)
REMEMBER_COOKIE_DURATION = timedelta(days=7)
