#! usr/local/bin/python
import sqlite3
from flask import Flask, session, g, config, render_template, request, redirect, url_for


DEBUG = True
DATABASE = 'coursecat.db'
app = Flask(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with open(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if DEBUG:
    init_db()
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request():
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    cursor = g.db.execute('select name, url, description from courses order by id desc')
    courses = [dict(name=row[0], url=row[1], description=row[2]) for row in cursor.fetchall()]
    return render_template('home.html', courses=courses)

@app.route('/courses/add', method="POST")
def post_course():
    g.db.execute('insert into courses (name, url, description) values (?, ?, ?)', 
            request.form['name'], request.form['url'], request.form['description'])
    g.db.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5001)