import os

_basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'coursecat_working.db')
SECRET_KEY = 'devkey'
