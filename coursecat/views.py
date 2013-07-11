#! usr/local/bin/python
from coursecat import app, db
from coursecat.models import Course, Topic
from flask.ext.wtf import Form, TextField, ValidationError, Required
from flask import render_template, request, redirect, url_for

class SubmitForm(Form):
    name = TextField('Name', description='Short title of course/tutorial')
    url = TextField('URL', description='Where can the course/tutorial be found on the web?')

@app.route('/')
def home():
    form = SubmitForm()
    return render_template('courses.html', courses=Course.query.all(), form=form)

@app.route('/topics')
def topics():
    form = SubmitForm()
    return render_template('topics.html', topics=Topic.query.all(), form=form)

# course for a particular topic:
@app.route('/topics/<topic_name>')
def topic(topic_name):
    form = SubmitForm()
    topic = Topic.query.filter_by(name=topic_name).first() #should only have one
    return render_template('courses.html', courses = topic.courses, form=form)

@app.route('/courses/add', methods=["GET","POST"])
def post_course():
    new_course = Course(name=request.form['name'], url=request.form['url'], description="description")
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('home'))
