from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from recycle_marketplace import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    items = db.relationship('Item', backref='owner', lazy='dynamic')
    reviews = db.relationship('Review', backref='reviewed', lazy='dynamic')

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id: int):
    return User.query.get(int(id))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(500))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title: str, description: str, price: float, owner: User):
        self.title = title
        self.description = description
        self.price = price
        self.owner = owner

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    rating = db.Column(db.Integer)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, reviewer: User, reviewed: User, content: str, rating: int):
        self.reviewer = reviewer
        self.reviewed = reviewed
        self.content = content
        self.rating = rating
