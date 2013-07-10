from coursecat import db
from coursecat.models import *
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
			name="course_%d" % num, 
			url="course_%d_url" %num, 
			description="course_%d_description" % num
	)
	db.session.add(new_course)

def create_and_add_topic(subject):
	"""initializes topics to filler text
	if no number given, random number chose for topic"""
	new_topic = Topic(
			subject = "topic_subject_%s" % subject 
	)
	db.session.add(new_topic)

map(create_and_add_course, xrange(10))
map(create_and_add_topic, TEST_TOPIC_NAMES)

db.session.commit()
