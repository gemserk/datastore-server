'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

from com.gemserk.scores.model.profile import Profile
from com.gemserk.scores.model.score import Score

import cgi
import json

class UpdateProfile(webapp.RequestHandler):  
   
    def get(self):
        self.post()
     
    def post(self):
        
        privateKey = cgi.escape(self.request.get('privateKey'))
        profile = Profile.all().filter("privateKey =", privateKey).get()
        
        # should do nothing and tell no error, to avoid ppl searching for private keys?
        if(not profile):
            self.response.set_status(500, message="Can't find profile with key " + privateKey)
            return
        
        if (not profile.guest):
            self.response.set_status(500, message="Can't change an already registered profile when it is not guest")
            return
        
        profile.guest = False
        profile.name = cgi.escape(self.request.get('name'))
        
        profile.put()
        
        scores = Score.all()
        scores = scores.filter("profilePublicKey =", profile.publicKey)
        
        for score in scores:
            score.name = profile.name
            score.put()
        
        profileData = {'privateKey': profile.privateKey, 'publicKey': profile.publicKey, 'name':profile.name, 'guest': profile.guest }
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(json.dumps(profileData))

