from app import db
import enum

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     username = db.Column(db.String(50))
#     password = db.Column(db.String(50))
#     type = db.Column(db.String(50))

#     @property
#     def is_authenticated(self):
#         return True

#     @property
#     def is_active(self):
#         return True

#     @property
#     def is_anonymous(self):
#         return False

#     def get_id(self):
#         return str(self.id)


#     def __init__(self, name, username, password, type):
#         self.name = name
#         self.username = username
#         self.password = password
#         self.type = type

#     __mapper_args__ = {
#         'polymorphic_identity': 'users',
#         'polymorphic_on': type
#     }

class NewsStatusEnum(enum.Enum):
    pending='pending'
    real='real'
    fake='fake'

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500))
    requestNumber = db.Column(db.String)
    status = db.Column(db.String)#db.Enum(default=NewsStatusEnum.pending, nullable=False))

    def __init__(self, id, message, requestNumber) -> None:
        self.id = id
        self.message = message
        self.requestNumber = requestNumber
        self.status = 'pending'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'message': self.message,
            'requestNumber': self.requestNumber,
            'status': self.status
        }

    def __str__(self) -> str:
        return self.status
