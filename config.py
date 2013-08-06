import os

_basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'coursecat_working.db')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', SQLITE_DATABASE_URI)
SECRET_KEY = 'devkey'
DEBUG = True
