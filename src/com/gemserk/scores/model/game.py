'''
Created on 12/08/2010

@author: gemserk
'''

from google.appengine.ext import db

class Game(db.Model):
    gameKey = db.StringProperty()
    title = db.StringProperty()
