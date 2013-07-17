#! usr/local/bin/python
from coursecat import app, db
from coursecat.models import Course, Topic, TopicsCourses, TopicCourseStats
from flask.ext.wtf import Form, TextField, ValidationError, \
    Required, DataRequired, TextAreaField, SelectField
from flask.ext.wtf.html5 import URLField
from flask import render_template, request, redirect, url_for, session

DEFAULT_SCORE = 0

class SubmitForm(Form):
    name = TextField('Name', default="Course Name")
    url = URLField('URL', default="Url")
    description = TextAreaField('Description', default="Description")
    topics = SelectField(u'Topics')

@app.route('/')
def home():
    form = SubmitForm()
    courses = Course.query.all()
    topic_set = set()
    for c in courses:
        for t in c.topics:
            topic_set.add(t)
    topic_choices = list(topic_set)
    topic_choices.sort()
    form.topics.choices = [(t.id, t.name) for t in topic_choices]
    return render_template('home.html', courses=courses, form=form)

@app.route('/courses')
def courses():
    form = SubmitForm()
    return render_template('courses.html', form=form, topics=Topic.query.all())

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    if request.method == 'GET':
        return display_topics()
    elif request.method =='POST':
        return add_topic()

def display_topics():
    topics = Topic.query.all()
    topics.sort()
    return render_template('topics.html', topics=topics, form=SubmitForm())

def add_topic():
    name = request.form['name']
    description = request.form['description']
    new_topic = Topic(name=name, description=description)
    db.session.add(new_topic)
    if request.form.get('course_id', False):
        course = Course.query.get(request.form['course_id'])
        course.associate_topic(new_topic)
    print 'gets here?'
    db.session.commit()
    return redirect(url_for('topic', topic_name=new_topic.id))

@app.route('/topics/<topic_name>')
def topic(topic_name):
    topic =  Topic.get(topic_name)
    if topic:
        return render_template('courses.html', form=SubmitForm(), topics=[topic])
    else:
        pass #TODO handle 404 and other errors

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
    new_course = Course(name=request.form['name'], url=request.form['url'], description=request.form['description'])
    chosen_topic = Topic.query.filter_by(name=request.form['topics']).first()
    if chosen_topic:
        new_course.topics.append(chosen_topic)
    else:
        new_topic = Topic(name=request.form['topics'])
        db.session.add(new_topic)
        new_course.topics.append(new_topic)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('home'))
