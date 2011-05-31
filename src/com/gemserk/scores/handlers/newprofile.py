'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

from com.gemserk.scores.model.profile import Profile
import random

class NewProfile(webapp.RequestHandler):  
    def get(self):
        self.post()
     
    def post(self):

        number = (1000000 + random.random() * 8999999)
        
        profile = Profile()
        profile.name = "guest-%d" % number;
        profile.guest = True
        
        # 'filebackup_%d.tar.gz' % count

        profile.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(profile.key())
