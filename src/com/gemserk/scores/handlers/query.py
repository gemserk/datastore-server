'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

import cgi
import time

from django.utils import simplejson as json

from com.gemserk.scores.model.game import Game

from com.gemserk.scores.model import score as scoreDao

class Query(webapp.RequestHandler):  
    
    def get(self):
        gameKey = cgi.escape(self.request.get('gameKey'))
        game = Game.all().filter("gameKey =", gameKey).get()
        
        if(not game):
            self.response.set_status(500, message="Can't find game with key " + gameKey)
            return
        
        range = self.request.get('range')
        tags = self.request.get_all('tag')        
        limit = self.request.get_range('limit')
        ascending = self.request.get('ascending')
        
        if(ascending == "true"):
            order = "points"
        else:
            order = "-points"
            
        scores = scoreDao.get_scores(game, range, tags, order, limit)

        self.response.headers['Content-Type'] = 'text/plain'
        scoreList = []
        for score in scores:
            data = json.loads(score.data)
            scoreData = {'id': str(score.key()), 'profilePublicKey': score.profilePublicKey, 'name': score.name, 'tags':score.tags, 'points':score.points, 'timestamp':long(time.mktime(score.timestamp.timetuple())*1000), 'data':data}
            scoreList.append(scoreData)
        
        self.response.out.write(json.dumps(scoreList))
        
