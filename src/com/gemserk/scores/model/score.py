'''
Created on 12/08/2010

@author: gemserk
'''

from google.appengine.ext import db

from game import Game

class Score(db.Model):
    game = db.ReferenceProperty(Game, collection_name="scores")
    tags = db.StringListProperty()
    points = db.IntegerProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty()
    data = db.TextProperty()
    profilePublicKey = db.StringProperty()
