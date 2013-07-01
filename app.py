#! usr/local/bin/python
from flask.ext.wtf import Form, TextField, ValidationError, Required
import sqlite3
from pprint import pprint
from flask import Flask, session, g, config, render_template, request, redirect, url_for

app = Flask(__name__)
DEBUG = True
app.config['DATABASE'] = 'coursecat.db'
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'devkey'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with connect_db() as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if DEBUG:
    init_db()

class SubmitForm(Form):
    name = TextField('Name', description='Short title of course/tutorial')
    url = TextField('URL', description='Where can the course/tutorial be found on the web?')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(Exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    form = SubmitForm()
    cursor = g.db.execute('select name, url, description from courses order by id desc')
    courses = [dict(name=row[0], url=row[1], description=row[2]) for row in cursor.fetchall()]
    pprint(courses)
    return render_template('courselist.html', courses=courses, form=form)

@app.route('/courses/add', methods=["GET","POST"])
def post_course():
    print 'getitng a request'
    pprint(request.form)
    g.db.execute('insert into courses (name, url, description) values (?, ?, ?)', 
             (request.form['name'], request.form['url'], "description"))
    g.db.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5001)








