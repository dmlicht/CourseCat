#! usr/local/bin/python
from coursecat import app, db
from coursecat.models import Course, Topic, Score
from flask.ext.wtf import Form, TextField, ValidationError, Required, DataRequired
from flask.ext.wtf.html5 import URLField
from flask import render_template, request, redirect, url_for

DEFAULT_SCORE = 0

class SubmitForm(Form):
    name = TextField('Name', default="Name")
    url = URLField('URL', default="Url")
    description = TextField('URL', default="Description")

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
    topic = Topic.query.filter_by(name=topic_name).first_or_404() #should only have one
    courses = topic.courses
    for course in courses:
        score_row = Score.query.filter_by(course=course.name, topic=topic_name).first()
        course.score = (score_row and score_row.score) or DEFAULT_SCORE
    return render_template('courses.html', courses=courses, topic=topic, form=form )

#@app.route('/courses/<course_name>')
#def course(course_name):
#    course = Course.query.filter_by(name=course_name).first()
#    scores = []
#    for topic in course.topics:
#        scores.append(Score.query.filter_by(course=course.name, topic=topic.name))
#    return render_template('course_info.html', topics = course.topics, scores = scores)

@app.route('/courses/add', methods=["GET","POST"])
def post_course():
    new_course = Course(name=request.form['name'], url=request.form['url'], description="description")
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('home'))
