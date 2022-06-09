from sqlalchemy import delete
from app import db

from datetime import datetime, timedelta

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

class Solicitation(db.Model):
    __tablename__ = 'solicitations'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    url = db.Column(db.String)
    response = db.Column(db.String)
    status = db.Column(db.String)#db.Enum(default=NewsStatusEnum.pending, nullable=False))
    created_at = db.Column(db.DateTime)
    responded_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __init__(self, message, url) -> None:
        self.message = message
        self.url = url
        self.response = None
        self.status = 'Pending'
        self.category_id = 1
        self.created_at = datetime.utcnow() - timedelta(hours=3)
        self.responded_at = None
        self.updated_at = None

    def set_category(self, category_id):
        self.category_id = category_id
        self.save()      
    
    def save(self) -> None:
        if self.responded_at is None:
            self.responded_at = datetime.utcnow() - timedelta(hours=3)
        self.updated_at = datetime.utcnow() - timedelta(hours=3)
        db.session.add(self)
        db.session.commit()

    def update(self, response=None, status=None, category_id=None) -> None:
        if response:
            self.response = response
        if status:
            self.status = status
        if category_id:
            self.set_category(category_id=category_id)
        self.save()
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()         

    def json(self) -> dict:
        return {
            'id': self.id,
            'message': self.message,
            'url': self.url,
            'response': self.response,
            'status': self.status,
            'category': self.category.name
        }
        
    
    def __str__(self) -> str:
        return self.status

    def __repr__(self) -> str:
        return f"Pedido: {self.id}, Status: {self.status}"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    solicitations = db.relationship('Solicitation', backref='category', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'solicitations': [solicitation.json() for solicitation in self.solicitations]
        }

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Categoria: {self.name}"