'''
Created on 12/08/2010

@author: gemserk
'''

from google.appengine.ext import db

from game import Game

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
    
def get_scores(game, range, tags, order, limit, year, month, week, day, rangeNumber=None, distinct=True):
    scoresQuery = game.scores
    
    if (range == "day"):
        if (rangeNumber is not 0):
            day = rangeNumber
        scoresQuery.filter("year =", year)
        scoresQuery.filter("day =", day)

    if (range == "week"):
        if (rangeNumber is not 0):
            week = rangeNumber
        scoresQuery.filter("year =", year)
        scoresQuery.filter("week =", week)

    if (range == "month"):
        if (rangeNumber is not 0):
            month = rangeNumber
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
