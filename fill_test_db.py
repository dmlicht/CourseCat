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

#map(create_and_add_course, xrange(10))
#map(create_and_add_topic, TEST_TOPIC_NAMES[:4])
#map(create_and_add_topic_with_courses, TEST_TOPIC_NAMES[4:])
create_course_with_two_topics_and_scores('GitHub Flow', 
	'http://scottchacon.com/2011/08/31/github-flow.html', 
	'describes good practices for working with git and github',
	'git', 'github')
create_course_with_two_topics_and_scores('Flask Mega-Tutorial',
	'http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world',
	'delves deeply into designing a web app in Flask',
	'flask', 'python')

db.session.commit()
