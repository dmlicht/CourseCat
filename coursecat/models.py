from coursecat import db

class Course(db.Model):
    """gives your object special properties, says Nina"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    url = db.Column(db.String(1000))
    description = db.Column(db.String(5000))

    def __repr__(self):
        return self.name

