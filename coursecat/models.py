from coursecat import db
from sqlalchemy.ext.associationproxy import association_proxy

class Course(db.Model):
    """gives your object special properties, says Nina"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    url = db.Column(db.String(1000))
    description = db.Column(db.String(5000))
    topics = association_proxy("assoc","topic")

    def __repr__(self):
        return self.name

class Topic(db.Model):
    """categories of courses"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(5000))
    courses = association_proxy("assoc", "course")

    def __repr__(self):
        return self.name


# association table:
class Assoc(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    course = db.relation(Course, backref = "assoc")
    topic = db.relation(Topic, backref = "assoc")
    score = db.Column(db.Integer)
