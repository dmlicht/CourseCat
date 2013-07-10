from coursecat import db
from coursecat.models import *

def create_and_add_course(num):
	new_course = Course(name="course_%d" % num, url="course_%d_url" %num, description="course_%d_description" % num)
	db.session.add(new_course)

for ii in xrange(10):
	create_and_add_course(ii)

db.session.commit()
