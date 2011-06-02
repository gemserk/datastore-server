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
import datetime

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
            
        filteredScores = game.scores
        
        year, month, week, day = dateutils.get_datetime_data(datetime.datetime.now())
        
        if (range == "day"):
            filteredScores.filter("day =", day)

        if (range == "week"):
            filteredScores.filter("week =", week)

        if (range == "month"):
            filteredScores.filter("month =", month)
            
        for tag in tags:
            filteredScores = filteredScores.filter("tags =", tag)

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
        
