from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
import cgi
import json
import time

class Game(db.Model):
    gameKey = db.StringProperty()
    title = db.StringProperty()
    
    
class Score(db.Model):
    game = db.ReferenceProperty(Game, collection_name="scores")
    tags = db.StringListProperty()
    points = db.IntegerProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty()
    data = db.TextProperty()
    

class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        
       
        games = list()
        
        for game in Game.all():
            games.append(game)
      
      
        template_values = {'games':games}

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
        score.game = game
        score.put()
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(score.key())


class Query(webapp.RequestHandler):  
    def get(self):
        gameKey = cgi.escape(self.request.get('gameKey'))
        game = Game.all().filter("gameKey =", gameKey ).get()
        
        if(not game):
            self.response.set_status(500,message="Can't find game with key " + gameKey)
            return
        
        tags = self.request.get_all('tag')
        
        limit = self.request.get_range('limit')
        ascending = self.request.get('ascending')
        if(ascending == "true"):
            order = "points"
        else:
            order =  "-points"
            
        filteredScores = game.scores
        for tag in tags:
            filteredScores = filteredScores.filter("tags =", tag)
            
        sortedScores = filteredScores.order(order)
        scores = sortedScores.fetch(limit)
        
        self.response.headers['Content-Type'] = 'text/plain'
        scoreList = []
        for score in scores:
            data = json.loads(score.data)
            scoreData = {'id': str(score.key()), 'name': score.name, 'tags':score.tags, 'points':score.points, 'timestamp':long(time.mktime(score.timestamp.timetuple())*1000), 'data':data}
            scoreList.append(scoreData)
        
        self.response.out.write(json.dumps(scoreList))


      
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
        
       
          
            
      
        
      


application = webapp.WSGIApplication([('/', MainPage), ('/init', InitDB),("/game",ShowGame), ("/submit",SubmitScore),("/scores",Query)], debug=True)


def main():
    
    
    
    run_wsgi_app(application)

if __name__ == "__main__":
    main()





