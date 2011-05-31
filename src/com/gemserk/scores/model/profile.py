'''
Created on 12/08/2010

@author: gemserk
'''

from google.appengine.ext import db

class Profile(db.Model):
    name = db.StringProperty()
    guest = db.BooleanProperty()
