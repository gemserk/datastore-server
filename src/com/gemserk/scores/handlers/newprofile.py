'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

from com.gemserk.scores.model.profile import Profile

import uuid
import cgi
import json

class NewProfile(webapp.RequestHandler):  
    def get(self):
        self.post()
     
    def post(self):
        profile = Profile()
        
        profile.privateKey = str(uuid.uuid4())
        profile.publicKey = str(uuid.uuid4())
        profile.name = cgi.escape(self.request.get('name'))
        
        has_guest = self.request.get('guest', 0)
        if has_guest == 0 or has_guest == "false":
            profile.guest = False
        else:
            profile.guest = True
        
        profile.put()

        profileData = {'privateKey': profile.privateKey, 'publicKey': profile.publicKey, 'name':profile.name, 'guest': profile.guest }
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(json.dumps(profileData))

