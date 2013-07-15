from coursecat import db


topics = db.Table('topics',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
)


class Course(db.Model):
    """create new course"""
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    url = db.Column(db.String(1000))
    description = db.Column(db.String(5000))
    topics = db.relationship('Topic', secondary=topics, backref=db.backref('courses'))

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

class Score(db.Model):
    __tablename__ = 'score'
    course_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    
