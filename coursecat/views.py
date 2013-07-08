#! usr/local/bin/python
from coursecat import app, db
from coursecat.models import Course
from flask.ext.wtf import Form, TextField, ValidationError, Required
from flask import render_template, request, redirect, url_for

class SubmitForm(Form):
    name = TextField('Name', description='Short title of course/tutorial')
    url = TextField('URL', description='Where can the course/tutorial be found on the web?')

@app.route('/')
def home():
    form = SubmitForm()
    return render_template('courselist.html', courses=Course.query.all(), form=form)

@app.route('/courses/add', methods=["GET","POST"])
def post_course():
    new_course = Course(name=request.form['name'], url=request.form['url'], description="description")
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('home'))