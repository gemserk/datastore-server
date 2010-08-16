'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

import cgi

from com.gemserk.scores.model.game import Game

class NewGame(webapp.RequestHandler):
    
    def post(self):
        gameKey = cgi.escape(self.request.get('gameKey'))
        title = cgi.escape(self.request.get('title'))
        
        game = Game.all().filter("gameKey =", gameKey ).get()
        
        if (game):
            self.response.headers['Content-Type'] = 'text/plain'        
            self.response.out.write("ERROR: gameKey already used")    
            return        
        
        game = Game()
        game.gameKey = gameKey
        game.title = title
        
        game.put()

        self.redirect('/')
