from coursecat import db

class TopicsCourses(db.Model):
    """connects topics and courses stats object
    list of topics_courses related to a given object can be accessed via
    <course_var>.topics_courses --> [topics_courses] 
    <topic_var>.topics_courses --> [topics_courses]
    topics_course will allow navigation to related Course, Topic, or Stats objects
    via .course, .topic, .stats, respectively"""

    __tablename__ = 'topics_courses'
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    stats_id = db.Column(db.Integer, db.ForeignKey('topic_course_stats.id'), primary_key=True)
    course = db.relationship("Course", backref="topics_courses")
    topic = db.relationship("Topic", backref="topics_courses")
    stats = db.relationship("TopicCourseStats", backref="topics_courses")


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    url = db.Column(db.String(1000))
    description = db.Column(db.String(5000))

    # bellow allows access array of topics associated with given course via topics attribute of vice versa
    topics = db.relationship('Topic', secondary='topics_courses', backref=db.backref('courses'))

    def __repr__(self):
        return "<Course %s>" % self.name

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

    def get_sorted_topics_courses(self):
        """returns list of topics course objects sorted by the saved on the stats object"""
        return sorted(self.topics_courses, key=lambda course_topic: course_topic.stats.score, reverse=True)

    def __repr__(self):
        return "<Topic %s>" % self.name

    def __init__(self, name):
        self.name = name

    def __cmp__(self, other):
        if self.name == other.name:
            return 0
        elif self.name > other.name:
            return 1
        else:
            return -1

class TopicCourseStats(db.Model):
    __tablename__ = 'topic_course_stats'
    id = db.Column(db.Integer, primary_key=True)
    #topics_courses_id = db.Column(db.Integer, db.ForeignKey('topics_courses.id'))
    score = db.Column(db.Integer)
    num_votes = db.Column(db.Integer)

    def __repr__(self):
        return "<Stats %d / %d>" % (self.score, self.num_votes)
