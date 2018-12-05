import os
import csv
from cosa.nlp.functions import *
import io
import sys
import time

"""Returns a double"""
def matchTerms(queryLabel, nodeLabel, model, number):
    start_time = time.time()
    # Get terms from query
    q = text2terms (queryLabel)
    t = text2terms (nodeLabel)
    qsize = len(q)
    nsize = len(t)
    tfreq = 0.0
    this_time = time.time()    
    print "terms calculated", str(this_time - start_time)
    
    for ttt in t:
        dic = model.similarToTerm(ttt, number)
        for qt in q:
            if not isinstance(qt, unicode):
                qt = unicode(qt, "utf-8")
            if qt in dic:
                tfreq += dic[qt]
    
    this_time2 = time.time()    
    print "freq calculated", str(this_time2 - this_time)
    
    # Formula
    score = ((tfreq / nsize) + (tfreq / qsize)) / 2
    this_time3 = time.time()    
    print "score calculated", str(this_time3 - this_time2)
    
    return score


def __matchEntities(queryEntities, nodeEntities, key):
    entsScore = 0.0;
    for qek in queryEntities:
        qentity = queryEntities[qek]
        qscore = float(qentity['score'])
        for nek in nodeEntities:
            nentity = nodeEntities[nek]
            nscore = float(nentity['score'])
            qentss = set(qentity[key])
            nentss = set(nentity[key])
            uentss = qentss.union(nentss)
            ientss = qentss.intersection(nentss)
            score = ((float(len(ientss)) / float(len(uentss))) * nscore * qscore)
            entsScore += score
    return entsScore

def matchTypes(queryEntities, nodeEntities):
    return __matchEntities(queryEntities, nodeEntities, 'types')
            
def matchSubjects(queryEntities, nodeEntities):
    return __matchEntities(queryEntities, nodeEntities, 'subjects')

def matchEntities(queryEntities, nodeEntities):
    return ((matchTypes(queryEntities, nodeEntities) + matchSubjects(queryEntities, nodeEntities)) / 2)

def matchNodes(queryNode, categoryNode, method = 'entities', model = None, embeddings = 1000):
    if method == 'entities':
        queryEntities = queryNode['entities']
        categoryEntities = categoryNode['entities']    
        return matchEntities(queryEntities, categoryEntities)
    elif method == 'types':
        queryEntities = queryNode['entities']
        categoryEntities = categoryNode['entities']    
        return matchTypes(queryEntities, categoryEntities)
    elif method == 'subjects':
        queryEntities = queryNode['entities']
        categoryEntities = categoryNode['entities']    
        return matchSubjects(queryEntities, categoryEntities)
    elif method == 'terms':
        return matchTerms(queryNode['label'], categoryNode['label'], model, embeddings)        
    else:
        raise ValueError('Unknown method: ' + method)    