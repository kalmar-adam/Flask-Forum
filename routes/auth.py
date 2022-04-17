from flask import Blueprint, flash, request, session, render_template, redirect, url_for, g
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from models import *
from datetime import datetime
from UserData import UserData
bp=Blueprint('auth', __name__)

class MyProfile(MethodView):
    def get(self):
        if g.user.getValue('id')==None:
            return redirect(url_for('index'))
        user=User.query.filter_by(id=g.user.getValue('id')).first()
        return render_template('myprofile.html', user=user)
    def post(self):
        if g.user.getValue('id')==None:
            return redirect(url_for('index'))
        user=User.query.filter_by(id=g.user.getValue('id')).first()
        opw=None
        npw=None
        if "opw" in request.form and request.form["opw"]!="":
            if Bcrypt().check_password_hash(user.passw, request.form["opw"]):
                opw=request.form["opw"]
            else: flash("Invalid old password!", "error")
        else: flash("Old password is empty!","error")
        if "npw" in request.form and request.form["npw"]!="":
            npw=request.form["npw"]
        else: flash("New password is empty!","error")
        if opw != None and npw != None:
            user.passw=Bcrypt().generate_password_hash(npw)
            db.session.commit()
            flash("Password change OK!", "succes")
        return render_template('myprofile.html', user=user)
bp.add_url_rule("/myprofile",view_func=MyProfile.as_view("myprofile"))

@bp.route('/login',  methods=['POST','GET'])
def login():
    udata=g.user
    if udata.getValue("id")!=None:
        return redirect(url_for('index'))
    if request.method=="POST":
        u=User.query.filter_by(name=request.form["name"]).first()
        if u!=None and Bcrypt().check_password_hash(u.passw, request.form["pw"]):
            session.clear()
            session["name"]=request.form["name"]
            return redirect(url_for('index'))
        else:
            flash("Invalid name or password")
    return render_template('login.html')

@bp.route('/reg', methods=['POST','GET'])
def reg():
    if g.user.getValue("id"):
        return redirect(url_for('index'))
    if request.method=="POST":
        uname_ok=(request.form["name"]!="")
        if not uname_ok:
            flash("Name input is empty.")
        pass_ok=(request.form["pw1"]==request.form["pw2"] and request.form["pw1"]!="")
        if not pass_ok:
            flash("Password inputs are empty or not matching.")
        nameunique_ok=(User.query.filter_by(name=request.form["name"]).first()==None)
        if not nameunique_ok:
            flash("This user is already exist.")
        if pass_ok and uname_ok and nameunique_ok:
            new_user=User(name=request.form["name"], passw=Bcrypt().generate_password_hash(request.form["pw1"]), regdate=datetime.now())
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('reg.html')
@bp.route("/logout")
def logout():
    if g.user.getValue("id"):
        session.clear()
        return redirect(url_for('index'))
    return render_template('login.html')