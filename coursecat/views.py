#! usr/local/bin/python
from coursecat import app, db
from coursecat.models import Course, Topic, TopicsCourses, Stats
from flask.ext.wtf import Form, TextField, ValidationError, \
    Required, DataRequired, TextAreaField, SelectField
from flask.ext.wtf.html5 import URLField
from flask import render_template, request, redirect, url_for, session

DEFAULT_SCORE = 0

### form to submit new courses
class SubmitForm(Form):
    name = TextField('Name', default="Course Name")
    url = URLField('URL', default="Url")
    description = TextAreaField('Description', default="Description")

    @classmethod
    def update_topics(cls):
        cls.topics = SelectField(u'Topics', choices=[(t.id, t.name) for t in Topic.query.all()])        

@app.before_request
def update_form_topics():
    SubmitForm.update_topics()


### form to edit courses
class CourseEditForm(Form):
    @classmethod
    def customize_form(cls, course):
        """sets name url and description for form defaults"""
        cls.name = TextField('Name', default=course.name)
        cls.url = URLField('URL', default=course.url)
        cls.description = TextAreaField('Description', default=course.description)


### HOME PAGE ###
@app.route('/')
def home():
    return render_template('home.html', courses=Course.query.all(), course_add_form=SubmitForm())

### COURSES PAGE ###
@app.route('/courses')
def courses():
    topics = Topic.query.all()
    topics.sort()
    return render_template('courses.html', course_add_form=SubmitForm(), topics=topics)

### TOPICS PAGE ###
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

### TOPIC-SPECIFIC PAGES ###
@app.route('/topics/<topic_name>')
def topic(topic_name):
    topic =  Topic.get(topic_name)
    if topic:
        return render_template('courses.html', course_add_form=SubmitForm(), topics=[topic])
    else:
        pass #TODO handle 404 and other errors

### COURSE-SPECIFIC PAGES ###
@app.route("/courses/<course_id>", methods = ["GET"])
def view_course(course_id):
    course = Course.query.get(course_id)
    return render_template("course.html", course_add_form=SubmitForm(), course=course)

### UPVOTE/DOWNVOTE BUTTONS ###
@app.route("/vote", methods=["POST"])
def vote():
    stats_id = request.form['stats_id']
    stats = Stats.query.filter_by(id=stats_id).first()
    stats.handle_vote(direction = request.form['vote'])
    return redirect(request.form['submitted_from'])

### BUTTON TO EDIT A COURSE ###
@app.route("/edit/<course_id>", methods=["GET","POST"])
def edit(course_id):
    course = Course.query.get(course_id)
    CourseEditForm.customize_form(course)
    return render_template("course.html", course_edit_form=CourseEditForm(), course=course)

### PAGE FOR SUBMITTING COURSE EDITS ###
@app.route("/courses/edit", methods=["GET", "POST"])
def edit_course():
    course = Course.query.get(request.form['course_id'])
    course.update(new_name = request.form['name'], new_url=request.form['url'], new_description=request.form['description'])
    db.session.commit()
    return redirect(url_for('view_course',course_id=course.id))

### PAGE FOR PROCESSING COURSE SUBMISSION FORM ###
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
