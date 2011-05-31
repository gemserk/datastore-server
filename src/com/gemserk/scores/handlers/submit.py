'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

import cgi

from com.gemserk.scores.model.game import Game
from com.gemserk.scores.model.score import Score

class SubmitScore(webapp.RequestHandler):  
    def get(self):
        self.post()
     
    def post(self):
        gameKey = cgi.escape(self.request.get('gameKey'))
        game = Game.all().filter("gameKey =", gameKey ).get()
        
        if(not game):
            self.response.set_status(500,message="Can't find game with key " + gameKey)
            return
        
        score = Score()
        score.name = cgi.escape(self.request.get('name'))
        score.tags = self.request.get_all('tag')
        score.points = self.request.get_range('points')
        score.data = cgi.escape(self.request.get('data'))
        profilePublicKey = self.request.get('profilePublicKey', None)
        if (profilePublicKey == None):
            score.profilePublicKey = None
        else:
            score.profilePublicKey = cgi.escape(profilePublicKey)
        score.game = game
        score.put()
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(score.key())
