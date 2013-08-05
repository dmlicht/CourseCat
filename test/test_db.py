import os
import sys
sys.path.append(os.path.abspath('../'))
import pytest
import coursecat
import tempfile
from coursecat.models import *


class TestDb:
    def setup_method(self, method):
        self.db_file_descriptor, coursecat.app.config["DATABASE"] = tempfile.mkstemp()
        coursecat.app.config["TESTING"] = True
        self.app = coursecat.app.test_client()
        coursecat.db.create_all()
        self.db = coursecat.db

    def teardown_method(self, method):
        os.close(self.db_file_descriptor)
        os.unlink(coursecat.app.config["DATABASE"])

    def add_commit(self, obj):
        """takes object, adds it to the database then commits"""
        self.db.session.add(obj)
        self.db.session.commit()

    @pytest.fixture
    def topic(self):
        return self.make_topic()

    @pytest.fixture
    def course(self):
        return self.make_course()
    
    def test_create_topic(self):
        self.make_topic()

    def make_topic(self, name="topic name", description="topic description"):
        """creates topic, adds to database and returns new topic"""
        new_topic = Topic(name, description)
        self.add_commit(new_topic)
        return new_topic

    def test_create_course(self):
        self.make_course()

    def make_course(self, name="course name", url="course url", description="c description"):
        """creates a course, adds it to the database and returns it"""
        new_course = Course(name, url, description)
        self.add_commit(new_course)
        return new_course

    def test_create_topics_courses_without_topic_or_course(self):
        with pytest.raises(Exception):
            new_topics_courses = TopicsCourses()
            self.add_commit(new_topics_courses)
        db.session.rollback()


    def test_create_topics_courses_with_topic_and_course(self, topic, course):
        new_topics_courses = TopicsCourses()
        new_topics_courses.topic = topic
        new_topics_courses.course = course
        new_topics_courses.stats = Stats()
        self.add_commit(new_topics_courses)

    def test_create_stats(self):
        assert Stats()

    #def test_associate_course_to_topic(self, topic, course):
    #    course.associate_topic(topic)

    #def test_create_user(self):
    #    new_user = User("name", "email")
    #    self.add_commit(new_user)

    def test_create_vote(self):
        assert Vote()
