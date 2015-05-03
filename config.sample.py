from os import path
from datetime import timedelta

top_dir = path.abspath(path.dirname(__file__))


mysql_info = {'database' : 'DATABASE',
              'server' : 'SERVER',
              'port' : 'PORT',
              'user' : 'USER',
              'password' : 'PASSWORD',
              'table_prefix' : 'TABLE_PREFIX',}

NUM_FEATURES = 10

PERMANENT_SESSION_LIFETIME = timedelta(minutes=24)
REMEMBER_COOKIE_DURATION = timedelta(days=7)
