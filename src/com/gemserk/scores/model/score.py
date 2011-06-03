'''
Created on 12/08/2010

@author: gemserk
'''

from google.appengine.ext import db

from game import Game

from  com.gemserk.scores.utils import dateutils
import datetime

class Score(db.Model):
    game = db.ReferenceProperty(Game, collection_name="scores")
    tags = db.StringListProperty()
    points = db.IntegerProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty()
    data = db.TextProperty()
    profilePublicKey = db.StringProperty()
    # used for filtering
    year = db.IntegerProperty()
    month = db.IntegerProperty()
    week = db.IntegerProperty()
    day = db.IntegerProperty()
    
def get_scores(game, range, tags, order, limit, distinct=True):
    scoresQuery = game.scores
    
    year, month, week, day = dateutils.get_datetime_data(datetime.datetime.now())
    
    if (range == "day"):
        scoresQuery.filter("year =", year)
        scoresQuery.filter("day =", day)

    if (range == "week"):
        scoresQuery.filter("year =", year)
        scoresQuery.filter("week =", week)

    if (range == "month"):
        scoresQuery.filter("year =", year)
        scoresQuery.filter("month =", month)
        
    for tag in tags:
        scoresQuery.filter("tags =", tag)
        
    scoresQuery = scoresQuery.order(order)
    
    scores = scoresQuery.fetch(limit)
    
    if (not distinct):
        return scores
    
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
        scores = scoresQuery.fetch(limit, offset)
        if (len(scores) == 0) :
            break
    
    return scores_distinct
