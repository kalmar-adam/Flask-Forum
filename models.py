from flask_sqlalchemy import *
from sqlalchemy import *

db=SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=True, nullable=False)
    passw=db.Column(db.String(100), nullable=False)
    role=db.Column(db.Integer, nullable=False, default=0)
    regdate=db.Column(db.DateTime, nullable=False)
    banned=db.Column(db.Integer, nullable=False, default=0)

    author=db.relationship('Comment', backref="user", cascade="all,delete")

class Topic(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=True, nullable=False)

    topic=db.relationship('Comment', backref="topic", cascade="all,delete")

class Comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.String(2000),  nullable=False)
    date=db.Column(db.DateTime, nullable=False)

    topic_id=db.Column(db.Integer, db.ForeignKey(Topic.id), nullable=False )
    user_id=db.Column(db.Integer, db.ForeignKey(User.id),  nullable=False )

    