from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#import os

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from coursecat import views

## we had to run the following in an interpreter:
# from coursecat import db
# from coursecat.models import *
# db.create_all()
##### first time only
