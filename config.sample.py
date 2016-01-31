from os import path, environ
from datetime import timedelta

## directory containing this file
TOP_DIR = path.abspath(path.dirname(__file__))

## Flask
PERMANENT_SESSION_LIFETIME = timedelta(minutes=24)
REMEMBER_COOKIE_DURATION = timedelta(days=7)
SECRET_KEY = 'onekeytorulethemalltrololol'

## MySQL
MYSQL_SERVER = 'localhost'
MYSQL_DATABASE = environ.get('MYSQL_DATABASE') or 'sgadx'
MYSQL_USER = environ.get('MYSQL_USER') or 'root'
MYSQL_PASS = environ.get('MYSQL_PASS') or 'taco'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}/{}'.format(MYSQL_USER,
                                                               MYSQL_PASS,
                                                               MYSQL_SERVER,
                                                               MYSQL_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False