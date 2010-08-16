from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import os
import cgi

from com.gemserk.scores.model.game import Game
from com.gemserk.scores.model.score import Score

from com.gemserk.scores.handlers.submit import SubmitScore
from com.gemserk.scores.handlers.query import Query
from com.gemserk.scores.handlers.newgame import NewGame

from google.appengine.api import users

class MainPage(webapp.RequestHandler):
    
    def get(self):
        games = list()
        
        for game in Game.all():
            games.append(game)
      
        isAdmin = users.is_current_user_admin()
      
        template_values = {'games':games, 'admin':isAdmin, 
                           'user':users.get_current_user(), 
                           'signInUrl':users.create_login_url('/'),
                           'signOutUrl':users.create_logout_url('/')}

        path = os.path.join(os.path.dirname(__file__), 'gameList.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, template_values))
      
class ShowGame(webapp.RequestHandler):
    
    def get(self):
        gameKey = cgi.escape(self.request.get('gameKey'))
        game = Game.all().filter("gameKey =", gameKey ).get()
        scores = game.scores.order('-points').fetch(1000)
        
        template_values = {'game':game, 'scores':scores}

        path = os.path.join(os.path.dirname(__file__), 'game.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, template_values))
     
class InitDB(webapp.RequestHandler):
    
    def get(self):
        newGame = Game()
        newGame.title = "test1"
        newGame.gameKey = "dsadfasfdsfaasd"
        newGame.put()
        
        score = Score()
        score.game = newGame
        score.tags = ["hard", "level1"]
        score.points = 10000
        score.name = "jtester"
        score.put()
        
        self.response.headers['Content-Type'] = 'text/plain'        
        self.response.out.write("OK") 

application = webapp.WSGIApplication([('/', MainPage), 
                                      ('/init', InitDB),
                                      ("/game",ShowGame), 
                                      ("/submit",SubmitScore),
                                      ("/scores",Query),
                                      ("/newGame",NewGame)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
