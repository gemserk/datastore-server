'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

import cgi
import time

from django.utils import simplejson as json

from com.gemserk.scores.model.game import Game

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
                
        # TODO: make it work with private_id instead user name         
        scores_distinct_names = []
        scores_distinct = []
        
        offset = 0
        while len(scores_distinct) < limit:
            for score in scores:
                if score.name not in scores_distinct_names and len(scores_distinct) < limit:
                    scores_distinct.append(score)
                    scores_distinct_names.append(score.name)
            offset += limit
            scores = sortedScores.fetch(limit, offset)
            if (len(scores) == 0) :
                break
        
        self.response.headers['Content-Type'] = 'text/plain'
        scoreList = []
        for score in scores_distinct:
            data = json.loads(score.data)
            scoreData = {'id': str(score.key()), 'name': score.name, 'tags':score.tags, 'points':score.points, 'timestamp':long(time.mktime(score.timestamp.timetuple())*1000), 'data':data}
            scoreList.append(scoreData)
        
        self.response.out.write(json.dumps(scoreList))
        