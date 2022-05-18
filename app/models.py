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
    phoneNumber = db.Column(db.String)
    requestNumber = db.Column(db.String)
    response = db.Column(db.String)
    status = db.Column(db.String)#db.Enum(default=NewsStatusEnum.pending, nullable=False))

    def __init__(self, message, phoneNumber, requestNumber) -> None:
        self.message = message
        self.phoneNumber = phoneNumber
        self.requestNumber = requestNumber
        self.response = None
        self.status = 'Pending'
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self, response=None, status=None) -> None:
        if response:
            self.response = response
        if status:
            self.status = status
        self.save()
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()         

    def json(self) -> dict:
        return {
            'id': self.id,
            'message': self.message,
            'phoneNumber': self.phoneNumber,
            'requestNumber': self.requestNumber,
            'status': self.status
        }
    
    def __str__(self) -> str:
        return self.status

    def __repr__(self) -> str:
        return f"Pedido: {self.requestNumber}, Status: {self.status}"
