#from secrets import token_hex
from flask import Flask, Blueprint, redirect, render_template, request, session, g, url_for
from flask_bcrypt import Bcrypt
from models import *
from routes import auth, comments, admin
from UserData import UserData

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

# secret key must be secret. generated via token_hex()
app.secret_key="226712672ffdabfa08b8ed369e2ac0d1f8f650a97baf2cf3cbd37d954bc4f1fc"


db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(comments.bp)
app.register_blueprint(admin.bp)

# get user datas every request to handle login and permissions
@app.before_request
def br():
    user=UserData(db)
    g.user=user

@app.route('/')
def index():
    udata=g.user
    stmt="""
        select t.id, t.name, t.lastcommentdate from
            (select topic.id, topic.name, ifnull(max(comment.date),'NO POST') as lastcommentdate from topic 
            left join comment on comment.topic_id=topic.id group by topic.name) as t
        order by t.lastcommentdate desc
    """
    topics=db.session.execute(stmt, {"uid":udata.getValue("id")}).all()
    return render_template('index.html', t=topics)

@app.errorhandler(404)
def notfound(e):
    return redirect(url_for('index'))

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(port=3000, debug=True)