from datetime import datetime
from flask import Flask, Blueprint, render_template
from flask_bcrypt import Bcrypt
from models import db
from app import *
import os
def do():
    #os.system("del db.sqlite3")
    db.create_all()
    db.session.add(User(name="admin", passw=Bcrypt().generate_password_hash("asd"), role=1, regdate=datetime.now()))
    db.session.add(User(name="testuser",passw=Bcrypt().generate_password_hash("asd"), role=0, regdate=datetime.now()))
    db.session.add(Topic(name="General"))
    db.session.add(Topic(name="New Topic"))
    db.session.add(Topic(name="Third Topic"))
    for i in range(0,236):
        sz="TEXT "+str(i)
        db.session.add(Comment(text=sz, date=datetime.now(), topic_id=1, user_id=1))

    db.session.commit()
with app.app_context():
    do()