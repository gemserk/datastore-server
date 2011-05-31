'''
Created on 12/08/2010

@author: gemserk
'''

from google.appengine.ext import db

class Profile(db.Model):
    privateKey = db.StringProperty()
    publicKey = db.StringProperty()
    name = db.StringProperty()
    guest = db.BooleanProperty()
