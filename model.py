#coding=utf-8
import logging

from google.appengine.ext import db, deferred
from google.appengine.api import users

class Topic(db.Model):
    author = db.UserProperty()
    sentence = db.StringProperty(multiline=True)
    answer = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    voteup = db.IntegerProperty()
    votedown = db.IntegerProperty()

    def can_vote(self):
        user = users.get_current_user()
        if not user:
            return False

        if user == self.author:
            return False

        vote = Vote.all()
        vote.filter('topic =', self.key())
        vote.filter('author =', user)
        result = vote.get()
        if result:
            return False
        return True

class Vote(db.Model):
    author = db.UserProperty()
    topic = db.ReferenceProperty(Topic)
    mark = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

