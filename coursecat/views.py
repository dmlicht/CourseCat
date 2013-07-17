#! usr/local/bin/python
from coursecat import app, db
from coursecat.models import Course, Topic, TopicsCourses
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

def getStats(topic_name):
    return db.session.query(Course, Topic, Stats).join(TopicsCourses).join(Topic).join(Stats).filter(Topic.name==topic_name).all()

# course for a particular topic:
@app.route('/topics/<topic_name>')
def topic(topic_name):
    form = SubmitForm()
    topic = Topic.query.filter_by(name=topic_name).first_or_404() #should only have one
    courses = topic.courses
    def right_topic(x):
        return x[1] == topic
    scores = filter(right_topic, getStats(topic.name))
    for c,t,s in scores:
        c.stats = s
    return render_template('courses.html', courses=courses, topicset=[topic], form=form)

@app.route("/courses/<course_name>", methods = ["GET", "POST"])
def view_course(course_name):
    form = SubmitForm()
    course = Course.query.filter_by(name=course_name).first_or_404()
    topic = course.topics[0]
    score_obj = Score.query.filter_by(course_id=course.id, topic_id=topic.id).first()
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


@app.route("/vote", methods=["POST"])
def vote():
    topic_id = request.form['topic_id']
    course_id = request.form['course_id']
    score = Score.query.filter_by(course_id=course_id, topic_id=topic_id).first()
    score = score or Score(course_id=course_id, topic_id=topic_id, score=DEFAULT_SCORE)
    score_change = 1 if (request.form["vote"] == "up") else -1
    score.score += score_change
    db.session.commit()
    print request.form['submitted_from']
    return redirect(request.form['submitted_from'])

@app.route('/courses/add', methods=["GET","POST"])
def post_course():
    new_course = Course(name=request.form['name'], url=request.form['url'], description="description")
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('home'))
