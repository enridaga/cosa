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
    tfOVERns = (tfreq / nsize) if nsize > 0 else 0.0
    tfOVERqs = (tfreq / qsize) if qsize > 0 else 0.0
    score = (tfOVERns + tfOVERqs) / 2
    return score

def __weightedSize(entitySet):
    total = 0.0
    #print list(entitySet)
    for item in entitySet:
        #print item
        total += 1.0 / float(entitySet[item])
    return total

def __intersection(qents,nents):
    size = 0.0
    for qek in qents:
        for nek in nents:
            if qek == nek:
                '''
                qents[qek] = a = query item distance
                nents[qek] = b = catalogue node item distance
                significance of q item = 1/a
                significance of n item = 1/b
                (1/a + 1/b) / 2 = 1/(2a) + 1/(2b)
                '''
                a = float(qents[qek])
                b = float(nents[nek])
                factor = (1/(2 * a)) + (1/(2 * b))
                size += 1.0 * factor
    return size

def __matchEntities(queryEntities, nodeEntities, key):
    entsScore = 0.0;
    for qek in queryEntities:
        qentity = queryEntities[qek]
        qscore = float(qentity['score'])
        for nek in nodeEntities:
            nentity = nodeEntities[nek]
            nscore = float(nentity['score'])
            #qentss = set(qentity[key])
            #nentss = set(nentity[key])
            #uentss = qentss.union(nentss)
            #ientss = qentss.intersection(nentss)
            '''
            entity score = ( (wM/wQS) + (wM/wNS) ) / 2
            (then all mutiplied by both the qEntitiy relevancy score and nEntity relevancy score)
            where...
                wM = weightedMatches (number of matches weighted for distance)
                wQS = weighted size of total query node URIs
                wNS = weighted size of total catalogue node URIs
            '''
            #score = ((float(len(ientss)) / float(len(uentss))) * nscore * qscore)
            #score = ((float(len(ientss)) / float(len(uentss))) * nscore * qscore)
            #score = (((__weightedSize(ientss)/__weightedSize(qentss)) + (__weightedSize(ientss)/__weightedSize(nentss))) / 2) * nscore * qscore
            wM = __intersection(qentity[key],nentity[key])
            wQS = __weightedSize(qentity[key])
            wNS = __weightedSize(nentity[key])
            if wQS > 0:
                wMwQS = wM/wQS
            else:
                wMwQS = 0
            if wNS > 0:
                wMwNS = wM/wNS
            else:
                wMwNS = 0
            score = ( ( wMwQS + wMwNS ) / 2 ) * nscore * qscore

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
            #Changing this to create embeddings from full description
            #ct = text2terms(categoryNode['label'])
            ct = text2terms(categoryNode['allDescriptions'])
            categoryNode['terms'] = ct
        return matchTerms(qt, ct, model, embeddings)        
    else:
        raise ValueError('Unknown method: ' + method)    