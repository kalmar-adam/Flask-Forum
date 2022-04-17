from flask import Blueprint, flash, request, session, render_template, redirect, url_for, g
from flask.views import *
from flask_bcrypt import Bcrypt
from UserData import UserData
from models import *
bp=Blueprint('admin', __name__)

# example for using MethodView
class AdminUser(MethodView):
    def get(self, userid=None):
        if g.user.getValue('role')!=1: return redirect(url_for('index'))
        if userid!=None:
            user=User.query.filter_by(id=userid).first()
            if "op" in request.args:
                if request.args["op"]=="ban":
                    user.banned=1
                if request.args["op"]=="unban":
                    user.banned=0
                db.session.commit()
            return redirect(url_for('admin.alluser'))
        else:
            users=User.query.all()
        return render_template('admin.html', users=users)
bp.add_url_rule("/admin/users", view_func=AdminUser.as_view('alluser'))
bp.add_url_rule("/admin/users/<int:userid>", view_func=AdminUser.as_view('oneuser'))



@bp.route("/admin/edittopic/<int:tid>", methods=["POST", "GET"])
def edittopic(tid):
    udata=g.user
    if udata.getValue('role')!=1:
        return redirect(url_for('index'))
    topic=Topic.query.filter_by(id=tid).first()
    if request.method=="POST" and request.form["tname"]!="":
        tname=request.form["tname"]
        db.session.execute("update or ignore topic set name=:tname where id=:tid", {"tname":tname,"tid":tid})
        db.session.commit()
    elif "t" in request.args and request.args["t"]=="delete":
        db.session.delete(Topic.query.filter(Topic.id==tid).first())
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('a_edittopic.html', topic=topic)

@bp.route("/admin/newtopic", methods=["POST", "GET"])
def newtopic():
    udata=g.user
    if udata.getValue('role')!=1:
        return redirect(url_for('index'))
    if (request.method=="POST" and request.form["tname"]!=""):
        tname=request.form["tname"]
        db.session.execute("""
            insert or ignore into topic (name) values (:tname)
        """, {"tname":tname})
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('a_newtopic.html')

@bp.route("/admin")
def admin():
    udata=g.user
    if udata.getValue('role')!=1:
        return redirect(url_for('index'))
    return render_template('admin.html')
