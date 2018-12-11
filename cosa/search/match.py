import os
import csv
from cosa.nlp.functions import *
import io
import sys
import time

"""Returns a double"""
def matchTexts(queryLabel, nodeLabel, model, number):
    #start_time = time.time()
    # Get terms from query
    q = text2terms (queryLabel)
    t = text2terms (nodeLabel)
    return matchTerms(q,t, model, number)

modelCache = {}

def matchTerms(queryTerms, nodeTerms, model, number):
    #start_time = time.time()
    # Get terms from query
    q = queryTerms
    t = nodeTerms
    qsize = len(q)
    nsize = len(t)
    tfreq = 0.0
    #this_time = time.time()    
    #print "terms calculated", str(this_time - start_time)
    global modelCache
    for ttt in t:
        if ttt in modelCache:
            dic = modelCache[ttt]
        else:
            dic = model.similarToTerm(ttt, number)
            modelCache[ttt] = dic
        for qt in q:
            if not isinstance(qt, unicode):
                qt = unicode(qt, "utf-8")
            if qt in dic:
                tfreq += dic[qt]
    # Formula
    score = ((tfreq / nsize) + (tfreq / qsize)) / 2
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
            if len(uentss) == 0:
                score = 0
            else:
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
        if 'terms' in queryNode:
            qt = queryNode['terms']
        else:
            qt = text2terms(queryNode['label'])
            queryNode['terms'] = qt
        if 'terms' in categoryNode:
            ct = categoryNode['terms']
        else:
            ct = text2terms(categoryNode['label'])
            categoryNode['terms'] = ct
        return matchTerms(qt, ct, model, embeddings)        
    else:
        raise ValueError('Unknown method: ' + method)    