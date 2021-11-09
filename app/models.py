from sqlalchemy.orm import backref
from werkzeug.datastructures import ContentRange
from app import db
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(300))
    # date_created = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=datetime.utcnow)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title=title
        self.content = content
        self.user_id = user_id

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(300))
    address = db.Column(db.String(500))
    phone_number = db.Column(db.Integer)
    date_created = db.Column(db.Integer, nullable=False, default=datetime.utcnow)

    def __init__(self, first, last, address, number):
        self.first= first
        self.last = last
        self.address = address
        self.number = number