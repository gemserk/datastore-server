'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

import cgi
import time

from django.utils import simplejson as json

from com.gemserk.scores.model.game import Game

from  com.gemserk.scores.utils import dateutils

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
            
        range = self.request.get_all('range')

        if (range == "day" or range == "week" or range == "month"):
            begin, end = dateutils.get_datetime_range(range)
            filteredScores.filter("timestamp >", begin)
            filteredScores.filter("timestamp <", end)
            
        sortedScores = filteredScores.order(order)
        scores = sortedScores.fetch(limit)
                
        scores_distinct_names = []
        scores_distinct = []
        
        offset = 0
        while len(scores_distinct) < limit:
            for score in scores:
                # if public key defined, then it is used to filter distinct entries         
                unique_id = score.profilePublicKey if (score.profilePublicKey != None) else score.name 
                if unique_id not in scores_distinct_names and len(scores_distinct) < limit:
                    scores_distinct.append(score)
                    scores_distinct_names.append(unique_id)
            offset += limit
            scores = sortedScores.fetch(limit, offset)
            if (len(scores) == 0) :
                break
        
        self.response.headers['Content-Type'] = 'text/plain'
        scoreList = []
        for score in scores_distinct:
            data = json.loads(score.data)
            scoreData = {'id': str(score.key()), 'profilePublicKey': score.profilePublicKey, 'name': score.name, 'tags':score.tags, 'points':score.points, 'timestamp':long(time.mktime(score.timestamp.timetuple())*1000), 'data':data}
            scoreList.append(scoreData)
        
        self.response.out.write(json.dumps(scoreList))
        