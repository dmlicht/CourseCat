from coursecat import db
from coursecat.models import *
db.create_all()
import random

TEST_TOPIC_NAMES = [
		"english",
		"history",
		"maths",
		"calculus",
		"github",
		"ruby on rails",
		"git",
		"ruby",
		"python",
		"numpy",
		"flask"
]
		
def create_and_add_course(num=-1):
	"""initializes courses to filler text
	if no number given, random number chose for course"""
	if num == -1:
		num = random.randint(0,1000)
	new_course = Course(
			name = "course_%d" % num, 
			url = "course_%d_url" %num, 
			description = "course_%d_description" % num
	)
	db.session.add(new_course)

def create_and_add_topic(name):
	"""initializes topics to filler text
	if no number given, random number chose for topic"""
	new_topic = Topic(
			name=name
	)
	db.session.add(new_topic)

def create_and_add_topic_with_courses(name):
	import random
	num = random.randint(0,1000)
	new_course = Course(
		name = 'course_%d' % num,
		url = 'www.awesome.com',
		description = 'description here'
	)
	new_topic = Topic(name=name)
	db.session.add(new_topic)
	db.session.add(new_course)
	new_topic.courses.append(new_course)

	second_course = Course(
		name = 'courseII_%d' % num,
		url = 'www.awesomesquared.com',
		description = 'description here AGAIN!'
	)

	new_topic.courses.append(second_course)

def create_course_with_two_topics_and_scores(name, url, description, *topics):
	new_course = Course(
		name = name,
		url = url,
		description = description
	)
	db.session.add(new_course)
	for t in topics:
		new_topic = Topic(name = t)
		db.session.add(new_topic)
		new_course.topics.append(new_topic)
		db.session.commit()
		rel = TopicsCourses(score=topics.index(t), course=new_course, topic=new_topic)
		db.session.add(rel)



def course_topic_test_fill_db():
    c = Course(name="Coursey", url="mytopicurl.com", description="the crazy course")
    c2 = Course(name="Courseo", url="mytopicuoorl.com", description="the crazy course")
    c3 = Course(name="Courseaaa", url="mytdjdopicuoorl.com", description="the crazy course")
    t = Topic(name="Intermediate video game playing")
    t2 = Topic(name="Git")
    db.session.add(c)
    db.session.add(c2)
    db.session.add(c3)
    db.session.commit()
    db.session.add(t)
    db.session.add(t2)
    tc = TopicsCourses()
    tc2 = TopicsCourses()
    tc3 = TopicsCourses()
    tc4 = TopicsCourses()
    tc.course = c
    tc.topic = t
    tc.stats = TopicCourseStats(score=100, num_votes=12)
    tc2.course = c2
    tc2.topic = t
    tc2.stats = TopicCourseStats(score=50, num_votes=30)
    tc3.course = c3
    tc3.topic = t
    tc3.stats = TopicCourseStats(score=20, num_votes=40)
    tc4.topic = t2
    tc4.course = c
    tc4.stats = TopicCourseStats(score=500, num_votes=501)
    db.session.add(tc)
    db.session.add(tc2)
    db.session.add(tc3)
    db.session.add(tc4)
    db.session.commit()

#map(create_and_add_course, xrange(10))
#map(create_and_add_topic, TEST_TOPIC_NAMES[:4])
#map(create_and_add_topic_with_courses, TEST_TOPIC_NAMES[4:])
#create_course_with_two_topics_and_scores('GitHub Flow', 
#	'http://scottchacon.com/2011/08/31/github-flow.html', 
#	'describes good practices for working with git and github',
#	'git', 'github')
#create_course_with_two_topics_and_scores('Flask Mega-Tutorial',
#	'http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world',
#	'delves deeply into designing a web app in Flask',
#	'flask', 'python')
#

course_topic_test_fill_db()

db.session.commit()
