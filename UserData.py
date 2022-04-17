from flask import session
from sqlalchemy import func
from models import *

class UserData():
    def __init__(self, database):
        self.db=database
        self.loggedname=self._getLoggedInName("name")
        self.userdata=None
        if self.loggedname!=None:
            tempQueryRes=self._getUserDatas(self.loggedname)
            if tempQueryRes!=None:
                self.userdata = { key:tempQueryRes[key] for key in tempQueryRes.keys()}
                #print(self.userdata)
            else:
                session.clear()

    def getValue(self, attr):
        if self.userdata!=None and attr in self.userdata:
            return self.userdata[attr]
        else: return None

    def _getLoggedInName(self, sess_key):
        if sess_key in session: return session[sess_key]
        else: return None

    def _getUserDatas(self, username):
        #return self.db.session.query(User.id, User.name, User.role, User.regdate).filter_by(name=username).first()
        return self.db.session.execute("""
            select user.id, user.name, user.role, user.regdate, user.banned
            from user where user.name=:uname
        """, {'uname':username}).first()
