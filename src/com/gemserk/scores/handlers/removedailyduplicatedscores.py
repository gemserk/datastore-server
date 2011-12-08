'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

from com.gemserk.scores.model.game import Game

import cgi

from com.gemserk.scores.utils import dateutils
from google.appengine.api import taskqueue

import datetime
        
class RemoveScoresForDayWorker(webapp.RequestHandler):
    def post(self): # should run at most 1/s
        
        gameKey = cgi.escape(self.request.get('gameKey'))
        game = Game.all().filter("gameKey =", gameKey).get()
        
        if(not game):
            return
        
        year, month, week, day = dateutils.get_datetime_data(datetime.datetime.now())
        
        tags = self.request.get_all('tag')
        day  = self.request.get('day')              
        limit = 1000
            
        scoresQuery = game.scores
            
        scoresQuery.filter("year =", year)
        scoresQuery.filter("day =", day)
            
        for tag in tags:
            scoresQuery.filter("tags =", tag)
        
        order = "-points"
            
        scoresQuery = scoresQuery.order(order)
        
        scores_distinct_names = []
        scores_unique = []
        
        offset = 0;
        scores = scoresQuery.fetch(limit, offset)
        
        while (len(scores) > 0):
            for score in scores:
                unique_id = score.profilePublicKey if (score.profilePublicKey != None) else score.name
                if unique_id not in scores_distinct_names:
                    scores_unique.append(score)
                    scores_distinct_names.append(unique_id)
                else:
                    score.delete()
            offset += limit
            scores = scoresQuery.fetch(limit, offset)
                

class RemoveDailyDuplicatedScores(webapp.RequestHandler):  
   
    def get(self):
        self.post()
     
    def post(self):
        
        gameKey = cgi.escape(self.request.get('gameKey'))
        game = Game.all().filter("gameKey =", gameKey).get()
        
        if(not game):
            self.response.set_status(500, message="Can't find game with key " + gameKey)
            return
        
        tags = self.request.get_all('tag')        
        
        year, month, week, today = dateutils.get_datetime_data(datetime.datetime.now())

        for day in range(today + 1):
            taskqueue.add(url='/removeScoresForDay', params={'gameKey': gameKey, 'tag': tags, 'day' : day})
            
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('OK - Tasks to remove scores for each day enqueued')
