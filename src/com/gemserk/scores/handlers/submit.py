'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

import cgi

from com.gemserk.scores.model.game import Game
from com.gemserk.scores.model.score import Score
from com.gemserk.scores.model.profile import Profile
import datetime
from com.gemserk.scores.utils import dateutils

class SubmitScore(webapp.RequestHandler):  
    def get(self):
        self.post()
     
    def post(self):
        gameKey = cgi.escape(self.request.get('gameKey'))
        game = Game.all().filter("gameKey =", gameKey ).get()
        
        if(not game):
            self.response.set_status(500,message="Can't find game with key " + gameKey)
            return
        
        currentTime = datetime.datetime.now()
        
        score = Score()
        score.name = cgi.escape(self.request.get('name'))
        score.tags = self.request.get_all('tag')
        score.points = self.request.get_range('points')
        score.data = cgi.escape(self.request.get('data', '{}'))
        score.profilePublicKey = self.request.get('profilePublicKey', None)
        
        profilePrivateKey = self.request.get('profilePrivateKey', None)
        
        if (profilePrivateKey <> None):
            profilePrivateKey = cgi.escape(profilePrivateKey)
            profile = Profile.all().filter("privateKey =", profilePrivateKey).get()

            if (profile <> None):
                score.profilePublicKey = profile.publicKey
                score.name = profile.name
                # update profile last access time
                profile.lastAccess = currentTime
                profile.put()
            else:
                self.response.set_status(500,message="Can't find profile to submit score")
                return
            
        score.year, score.month, score.week, score.day = dateutils.get_datetime_data(currentTime)
            
        score.game = game
        score.put()
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(score.key())
