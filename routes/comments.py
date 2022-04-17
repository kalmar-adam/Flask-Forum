from flask import Blueprint, flash, request, render_template, redirect, url_for, g
from models import *
from UserData import UserData
from datetime import datetime
from Pagination import Pagination
bp=Blueprint('comments', __name__)
#g.user

@bp.route("/topic/<int:tid>", methods=["GET","POST"])
def topic(tid):
    udata=g.user
    #check acces to topic and its comments
    stmt="""
        select t.id, t.tname, t.cc from
            (select topic.id, topic.name as tname, count(comment.id) as cc from topic left join comment
            on topic.id=comment.topic_id group by topic.id, topic.name) as t, user
        where t.id=:tid
    """
    acces=db.session.execute(stmt, {"uid":udata.getValue("id"), "tid":tid}).first()
    if acces==None:
        return redirect(url_for('index'))
    
    if request.method=="POST" and udata.getValue("id"):
        comment=request.form["c"].strip()
        if comment!="" and udata.getValue("banned")==0:
            c=Comment(text=comment, topic_id=tid, user_id=udata.getValue("id"), date=datetime.now())
            db.session.add(c)
            db.session.commit()
        if comment=="": flash("Comment can not be empty!")
        return redirect(url_for('comments.topic', tid=tid)+str("#down"))

    pag=None
    if "p" in request.args:
        pag=Pagination(acces.cc, int(request.args["p"]))
        if pag.isOutSide(int(request.args["p"])):
            return redirect(url_for('comments.topic', tid=tid))
    else: pag=Pagination(acces.cc)

    comments=db.session.execute("""
        select user.name as uname, comment.text, comment.date from comment, user, topic
        where comment.topic_id=topic.id and comment.user_id=user.id and topic.id=:tid
        limit :lim offset :offs 
    """, {"offs":(pag.actPage-1)*pag.perPage, "lim":pag.perPage, "tid":tid})
    return render_template("topic.html", pagination=pag, acces=acces, cs=comments, uinfo=udata)