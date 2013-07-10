from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'coursecat_working.db')
app.config['SECRET_KEY'] = 'devkey'
db = SQLAlchemy(app)

from coursecat import views

## we had to run the following in an interpreter:
# from coursecat import db
# from coursecat.models import *
# db.create_all()
##### first time only
