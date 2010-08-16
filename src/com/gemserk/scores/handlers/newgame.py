'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

import cgi

from com.gemserk.scores.model.game import Game

class NewGame(webapp.RequestHandler):
    
    def get(self):
        self.redirect('/')
    
    def post(self):
        gameKey = cgi.escape(self.request.get('gameKey')).strip()
        title = cgi.escape(self.request.get('title')).strip()
        
        game = Game.all().filter("gameKey =", gameKey ).get()

        error = ''
        
        if (game):
            error = error + "ERROR: gameKey already used\n"

        if (gameKey == ''):
            error = error + "ERROR: gameKey cannot be empty\n"

        if (title == ''):
            error = error + "ERROR: title cannot be empty\n"
        
        if (error != ''): 
            self.response.headers['Content-Type'] = 'text/plain'        
            self.response.out.write(error)    
            return
        
        game = Game()
        game.gameKey = gameKey
        game.title = title
        
        game.put()

        self.redirect('/')
