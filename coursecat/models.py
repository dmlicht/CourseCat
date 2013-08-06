from coursecat import db

class TopicsCourses(db.Model):
    """connects topics and courses stats object
    list of topics_courses related to a given object can be accessed via
    <course_var>.topics_courses --> [topics_courses] 
    <topic_var>.topics_courses --> [topics_courses]
    topics_course will allow navigation to related Course, Topic, or Stats objects
    via .course, .topic, .stats, respectively"""

    __tablename__ = 'topics_courses'
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True, nullable=False)
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id'), nullable=False)
    course = db.relationship("Course", backref="topics_courses")
    topic = db.relationship("Topic", backref="topics_courses")
    stats = db.relationship("Stats", backref="topics_courses")

    def __init__(self):
        self.stats = Stats()

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

    def associate(self, topic):
        """returns newly created topics_courses connected this course with given topic
        Also creates and adds a reference to a stats object from the topics_course"""
        new_topics_courses = TopicsCourses()
        new_topics_courses.topic = topic
        self.topics_courses.append(new_topics_courses)
        return new_topics_courses

    def update(self, new_name, new_url, new_description):
        self.name = new_name
        self.url = new_url
        self.description = new_description


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

    def associate(self, course):
        """returns newly created topics_courses connected this topic with given course
        Also creates and adds a reference to a stats object from the topics_course"""
        new_topics_courses = TopicsCourses()
        new_topics_courses.course = course
        self.topics_courses.append(new_topics_courses)
        return new_topics_courses

    def get_sorted_topics_courses(self):
        """returns list of topics course objects sorted by the saved on the stats object"""
        return sorted(self.topics_courses, key=lambda course_topic: course_topic.stats.score, reverse=True)

    def __repr__(self):
        return "<Topic %s>" % self.name

    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def __cmp__(self, other):
        if self.name.lower() == other.name.lower():
            return 0
        elif self.name.lower() > other.name.lower():
            return 1
        else:
            return -1


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    votes = db.relationship("Vote", backref="stats")
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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    email = db.Column(db.String(140))
    votes = db.relationship('Vote', backref='user')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def do_vote(self, stats, vote_val):
        """returns vote objects
        if vote already exists between user and stats entry, it will be updated with new given vote val and date
        if vote does not exist one will be instantiated with current user, given stats entry and given vote value"""
        vote = self.get_vote(stats)
        if vote is None:
            vote = Vote()
        vote.user = self
        vote.stats = stats
        vote.value = vote_val
        return vote

    #MAY BE INEFFICIENT
    def get_vote(self, stats):
        """returns a vote object connected to user and stats arguments
        returns None if there is no existing vote
        raise type error if argument is wrong type"""
        if not isinstance(stats, Stats):
            raise TypeError
        return Vote.query.filter_by(user_id=self.id, stats_id=stats.id).first()


class Vote(db.Model):
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    value = db.Column(db.Integer)

    @db.validates('value')
    def validate_value(self, key, value):
        assert (0 <= value <= 1)
