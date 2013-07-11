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

def create_course_with_two_topics_and_scores(name):
	new_course = Course(
		name = name,
		url = 'www.coursename.com',
		description = 'I am a course with two topics'
	)

	topic_1 = Topic(name = 'topic_1')
	topic_2 = Topic(name = 'topic_2')
	db.session.add(new_course)
	db.session.add(new_topic)
	new_course.topic.append(topic_1)
	new_course.topic.append(topic_2)

	db.session.add(Score(course=name, topic=topic_1.name, score=1))
	db.session.add(Score(course=name, topic=topic_2.name, score=2))
	


map(create_and_add_course, xrange(10))
map(create_and_add_topic, TEST_TOPIC_NAMES[:4])
map(create_and_add_topic_with_courses, TEST_TOPIC_NAMES[4:])

db.session.add(Score(course="course_0", topic=""))

db.session.commit()
