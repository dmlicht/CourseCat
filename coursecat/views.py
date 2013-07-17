#! usr/local/bin/python
from coursecat import app, db
from coursecat.models import Course, Topic, TopicsCourses, TopicCourseStats
from flask.ext.wtf import Form, TextField, ValidationError, \
    Required, DataRequired, TextAreaField
from flask.ext.wtf.html5 import URLField
from flask import render_template, request, redirect, url_for, session

DEFAULT_SCORE = 0

class SubmitForm(Form):
    name = TextField('Name', default="Name")
    url = URLField('URL', default="Url")
    description = TextAreaField('URL', default="Description")

@app.route('/')
def home():
    form = SubmitForm()
    return render_template('home.html', courses=Course.query.all(), form=form)

@app.route('/courses')
def courses():
    form = SubmitForm()
    return render_template('courses.html', form=form, topics=Topic.query.all())

@app.route('/topics')
def topics():
    form = SubmitForm()
    topics = Topic.query.all()
    topics.sort()
    return render_template('topics.html', topics=topics, form=form)

@app.route('/topics/<topic_name>')
def topic(topic_name):
    topic =  Topic.get(topic_name)
    return render_template('courses.html', form=SubmitForm(), topics=[topic])

@app.route("/courses/<course_id>", methods = ["GET"])
def view_course(course_id):
    course = Course.query.get(course_id)
    #I renamed course_single.html -> course.html
    #we can use plurality of the word distinguish between a single
    #element or a list
    return render_template("course.html", form=SubmitForm(), course=course)

@app.route("/vote", methods=["POST"])
def vote():
    stats_id = request.form['stats_id']
    stats = TopicCourseStats.query.filter_by(id=stats_id).first()
    score_change = 1 if (request.form["vote"] == "up") else -1
    stats.score += score_change
    stats.num_votes += 1
    db.session.commit()
    return redirect(request.form['submitted_from'])

@app.route('/courses/add', methods=["GET","POST"])
def post_course():
    new_course = Course(name=request.form['name'], url=request.form['url'], description="description")
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('home'))
