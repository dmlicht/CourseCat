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
    return render_template('home.html', courses=Course.query.all(), form=form)

@app.route('/courses')
def courses():
    form = SubmitForm()
    courses = Course.query.all()
    topicset = set()
    for course in courses:
        for topic in course.topics:
            topicset.add(topic)
    ### ADD SCORE UPDATING ABILITIES HERE
    topiclist = list(topicset)
    topiclist.sort()
    return render_template('courses.html', courses=courses, form=form, topicset=topiclist)

@app.route('/topics')
def topics():
    form = SubmitForm()
    topics = Topic.query.all()
    topics.sort()
    return render_template('topics.html', topics=topics, form=form)

# course for a particular topic:
@app.route('/topics/<topic_name>')
def topic(topic_name):
    form = SubmitForm()
    topic = Topic.query.filter_by(name=topic_name).first_or_404() #should only have one
    courses = topic.courses
    for course in courses:
        score_row = Score.query.filter_by(course=course.name, topic=topic_name).first()
        course.score = (score_row and score_row.score) or DEFAULT_SCORE
    return render_template('courses.html', courses=courses, topicset=[topic], form=form )

@app.route("/courses/<course_name>", methods = ["GET", "POST"])
def view_course(course_name):
    form = SubmitForm()
    course = Course.query.filter_by(name=course_name).first_or_404()
    if request.method == "POST":
        button_pressed = request.form['vote'].split(' ')
        score_obj = Score.query.filter_by(course=course.name, topic=button_pressed[1]).first()
        if button_pressed[0] == 'upvote': 
            score_obj.score += 1
        elif button_pressed[0] == 'downvote':
            score_obj.score -= 1
        else:
            print "there was a problem :("
    db.session.commit()
    scores_all_topics = [Score.query.filter_by(course=course.name, topic=t.name).first().score for t in course.topics]
    return render_template("course_single.html", course = course, form = form, scores = scores_all_topics)



@app.route('/courses/add', methods=["GET","POST"])
def post_course():
    new_course = Course(name=request.form['name'], url=request.form['url'], description="description")
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('home'))
