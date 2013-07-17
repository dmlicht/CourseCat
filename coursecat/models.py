from coursecat import db

class TopicsCourses(db.Model):
    __tablename__ = 'topics_courses'
    id =  db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    score = db.Column(db.Integer)
    course = db.relationship('Course', backref="topic_assocs")
    topic = db.relationship('Topic', backref="course_assocs")


class Course(db.Model):
    """create new course"""
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    url = db.Column(db.String(1000))
    description = db.Column(db.String(5000))

    def __repr__(self):
        return self.name

    def __init__(self, name, url, description):
        self.name = name
        self.url = url
        self.description = description


class Topic(db.Model):
    """categories of courses"""
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(5000))

    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.name = name

    def __cmp__(self, other):
        if self.name == other.name:
            return 0
        elif self.name > other.name:
            return 1
        else:
            return -1

# class Stats(db.Model):
#     __tablename__ = 'stats'
#     id = db.Column(db.Integer, primary_key=True)
#     topics_courses_id = db.Column(db.Integer, db.ForeignKey('topics_courses.id'))
#     score = db.Column(db.Integer)

#     def __repr__(self):
#         return str(self.score)

