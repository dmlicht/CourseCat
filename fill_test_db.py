from coursecat import db
from coursecat.models import *
db.create_all()
import random

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
    tc.stats = TopicCourseStats()
    tc2.course = c2
    tc2.topic = t
    tc2.stats = TopicCourseStats()
    tc3.course = c3
    tc3.topic = t
    tc3.stats = TopicCourseStats()
    tc4.topic = t2
    tc4.course = c
    tc4.stats = TopicCourseStats()
    db.session.add(tc)
    db.session.add(tc2)
    db.session.add(tc3)
    db.session.add(tc4)
    db.session.commit()

course_topic_test_fill_db()

db.session.commit()
