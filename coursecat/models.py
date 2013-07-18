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

    # below allows access array of topics associated with given course via topics attribute of vice versa
    topics = db.relationship('Topic', secondary='topics_courses', backref=db.backref('courses'))

    def __repr__(self):
        return "<Course %s>" % self.name

    def __init__(self, name, url, description):
        self.name = name
        self.url = url
        self.description = description

    def associate_topic(self, topic):
        """creates topics_course and stats object for a new association between courses and topics"""
        new_topics_course = TopicsCourses(topic = topic, stats = TopicCourseStats())
        self.topics_courses.append(new_topics_course)


class Topic(db.Model):
    """categories of courses"""
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(5000))

    @classmethod
    def get(cls, topic_info):
        """returns a topic given ID or name.
        ID can be string or int. returns None if topic can not be found."""
        try: #to treat topic info as topic.id
            return Topic.query.get(int(topic_info))
        except Exception: #treat topic info as topic.name
            return Topic.query.filter_by(name=topic_info).first()

    def associate_course(self, course):
        new_topics_course = TopicsCourses(course = course, stats=TopicCourseStats())
        self.topics_courses.append(new_topics_course)

    def get_sorted_topics_courses(self):
        """returns list of topics course objects sorted by the saved on the stats object"""
        return sorted(self.topics_courses, key=lambda course_topic: course_topic.stats.score, reverse=True)

    def __repr__(self):
        return "<Topic %s>" % self.name

    def __init__(self, name, description=""):
        self.name = name
        self.description = description

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
    num_upvotes = db.Column(db.Integer)
    num_votes = db.Column(db.Integer)
    score = db.Column(db.Float)

    def __repr__(self):
        return "<Stats %d / %d>" % (self.score, self.num_votes)

    def __init__(self):
        self.num_upvotes = 0
        self.num_votes = 0
        self.score = 0

    def update_score(self):
        import math
        z = 1.96 #95% CI
        phat = float(self.num_upvotes)/self.num_votes
        n = self.num_votes
        self.score = (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

    def handle_vote(self, direction):
        if direction != "up" and direction != "down":
            raise ValueError('direction must be up or down')
        if (direction == "up"):
            self.num_upvotes += 1
        self.num_votes += 1
        self.update_score()
        db.session.commit()

    def get_percent_positive(self):
        if self.num_votes > 0:
            return '{:.1%}'.format(float(self.num_upvotes)/self.num_votes)
        else: 
            return '0%'

