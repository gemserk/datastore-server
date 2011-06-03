import os
import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import cgi

from com.gemserk.scores.model.game import Game
from com.gemserk.scores.model.score import Score

from com.gemserk.scores.handlers.submit import SubmitScore
from com.gemserk.scores.handlers.query import Query
from com.gemserk.scores.handlers.newgame import NewGame
from com.gemserk.scores.handlers.newprofile import NewProfile
from com.gemserk.scores.handlers.updateprofile import UpdateProfile
from com.gemserk.scores.model.profile import Profile

from com.gemserk.scores.utils import dateutils

from com.gemserk.scores.model import score as scoreDao

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
        range = self.request.get('range')
        
        game = Game.all().filter("gameKey =", gameKey ).get()
        
        tags = self.request.get_all('tag')        
        limit = self.request.get_range('limit', 1000)
        
        # scores = game.scores
        
        scores = scoreDao.get_scores(game, range, tags, "points", limit)
        
        template_values = {'game':game, 'scores':scores}

        path = os.path.join(os.path.dirname(__file__), 'game.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, template_values))
     
class InitDB(webapp.RequestHandler):
    
    def score(self, game, name, tags, points, datetime):
        score = Score()
        score.game = game
        score.name = name
        score.points = points
        score.tags = tags
        score.data = "{}"
        score.timestamp = datetime
        score.year, score.month, score.week, score.day = dateutils.get_datetime_data(datetime.datetime.now())
        score.put()
        return score
    
    def get(self):
        newGame = Game()
        newGame.title = "test1"
        newGame.gameKey = "dsadfasfdsfaasd"
        newGame.put()
        
        self.score(newGame, "lastmonth-12341", ["hard"], 10000, datetime.datetime.today() - datetime.timedelta(days=40))
        self.score(newGame, "lastweek-15341", ["hard"], 15000, datetime.datetime.today() - datetime.timedelta(days=8))
        self.score(newGame, "yesterday-17341", ["hard"], 5000, datetime.datetime.today() - datetime.timedelta(days=2))
        self.score(newGame, "yesterday-17341", ["hard"], 7500, datetime.datetime.today() - datetime.timedelta(days=2))
        self.score(newGame, "yesterday-17341", ["hard"], 6500, datetime.datetime.today() - datetime.timedelta(days=1))
        self.score(newGame, "today-17341", ["hard"], 3500, datetime.datetime.today())
        
        self.response.headers['Content-Type'] = 'text/plain'        
        self.response.out.write("OK") 


class ProfileList(webapp.RequestHandler):
    
    def get(self):
        profiles = list()
        
        for profile in Profile.all():
            profiles.append(profile)
      
        isAdmin = users.is_current_user_admin()
      
        template_values = {'profiles':profiles, 'admin':isAdmin, 
                           'user':users.get_current_user(), 
                           'signInUrl':users.create_login_url('/'),
                           'signOutUrl':users.create_logout_url('/')}

        path = os.path.join(os.path.dirname(__file__), 'profileList.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, template_values))
   
class GenerateDateDateForScores(webapp.RequestHandler):
    
    def get(self):

        isAdmin = users.is_current_user_admin()
        
        if (not isAdmin):
            self.response.set_status(403, message="only admin can generate data for scores")
            return
        
        scores = Score.all()
        
        for score in scores:
            score.year, score.month, score.week, score.day = dateutils.get_datetime_data(score.timestamp)
            score.put()
      
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("OK")   
        
application = webapp.WSGIApplication([('/', MainPage), 
                                      ('/init', InitDB),
                                      ("/game",ShowGame),
                                      ("/profiles",ProfileList),  
                                      ("/submit",SubmitScore),
                                      ("/scores",Query),
                                      ("/newGame",NewGame),
                                      ("/newProfile", NewProfile),
                                      ("/updateProfile", UpdateProfile),
                                      ("/updateScores", GenerateDateDateForScores),
                                      ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
