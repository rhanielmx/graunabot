from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    type = db.Column(db.String(50))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


    def __init__(self, name, username, password, type):
        self.name = name
        self.username = username
        self.password = password
        self.type = type

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': type
    }
