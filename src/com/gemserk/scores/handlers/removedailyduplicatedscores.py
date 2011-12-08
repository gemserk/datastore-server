'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

from com.gemserk.scores.model.score import Score
from com.gemserk.scores.model.game import Game

import cgi

from com.gemserk.scores.utils import dateutils

import datetime

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
        limit = 100
        
        order = "-points"
        
        rangeNumber = self.request.get_range('rangeNumber')
         
        year, month, week, day = dateutils.get_datetime_data(datetime.datetime.now())

        scoresQuery = game.scores
            
        scoresQuery.filter("year =", year)
        scoresQuery.filter("day =", rangeNumber)
            
        for tag in tags:
            scoresQuery.filter("tags =", tag)
            
        scoresQuery = scoresQuery.order(order)
        
        scores = scoresQuery.fetch(limit)
        
        scores_distinct_names = []
        scores_unique = []
        
        # scores_remove = []

        offset = 0;
        while (len(scores) > 0):
            for score in scores:
                unique_id = score.profilePublicKey if (score.profilePublicKey != None) else score.name
                if unique_id not in scores_distinct_names:
                    scores_unique.append(score)
                    scores_distinct_names.append(unique_id)
                else:
                    score.delete()
                    # scores_remove.append(score)
            offset += limit
            scores = scoresQuery.fetch(limit, offset)
            
        # game.scores.remove(scores_remove)
    
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('OK')
