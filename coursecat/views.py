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

    @classmethod
    def update_topics(cls):
        cls.topics = SelectField(u'Topics', choices=[(t.id, t.name) for t in Topic.query.all()])        

#removed init function from submit form because it would crash database initialization
#This will update the topics listed
#in the submit form before every request.
@app.before_request
def update_form_topics():
    SubmitForm.update_topics()

@app.route('/')
def home():
    return render_template('home.html', courses=Course.query.all(), course_add_form=SubmitForm())

@app.route('/courses')
def courses():
    return render_template('courses.html', course_add_form=SubmitForm(), topics=Topic.query.all())

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    if request.method == 'GET':
        return display_topics()
    elif request.method =='POST':
        return add_topic()

def display_topics():
    topics = Topic.query.all()
    topics.sort()
    return render_template('topics.html', topics=topics)

def add_topic():
    name = request.form['name']
    description = request.form['description']
    new_topic = Topic(name=name, description=description)
    db.session.add(new_topic)
    if request.form.get('course_id', False):
        course = Course.query.get(request.form['course_id'])
        course.associate_topic(new_topic)
    db.session.commit()
    return redirect(url_for('topic', topic_name=new_topic.id))

@app.route('/topics/<topic_name>')
def topic(topic_name):
    topic =  Topic.get(topic_name)
    if topic:
        return render_template('courses.html', course_add_form=SubmitForm(), topics=[topic])
    else:
        pass #TODO handle 404 and other errors

@app.route("/courses/<course_id>", methods = ["GET"])
def view_course(course_id):
    course = Course.query.get(course_id)
    return render_template("course.html", course_add_form=SubmitForm(), course=course)

@app.route("/vote", methods=["POST"])
def vote():
    stats_id = request.form['stats_id']
    stats = TopicCourseStats.query.filter_by(id=stats_id).first()
    stats.handle_vote(direction = request.form['vote'])
    return redirect(request.form['submitted_from'])

@app.route('/courses/add', methods=["GET","POST"])
def post_course():
    new_course = Course(name=request.form['name'], url=request.form['url'], description=request.form['description'])
    chosen_topic = Topic.get(request.form['topics'])
    if chosen_topic:
        new_course.associate_topic(chosen_topic)
    else:
        new_topic = Topic(name=request.form['topics'])
        db.session.add(new_topic)
        new_course.associate_topic(new_topic)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('home'))
