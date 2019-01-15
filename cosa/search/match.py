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
    ntfreq = 0.0
    qtfreq = 0.0
    #this_time = time.time()    
    #print "terms calculated", str(this_time - start_time)
    global modelCache

    #Nested loop twice, once in each directions...
    #Loop nest 1...
    for ttt in t:
        if ttt in modelCache:
            dic = modelCache[ttt]
        else:
            dic = model.similarToTerm(ttt, number)
            modelCache[ttt] = dic

        #print "q: ",q
        #print "t: ",t
        #print "dic: ", dic
        #print "Press return to continue"
        #text = sys.stdin.readline()
        maxNTScore = 0.0
        for qt in q:
            if not isinstance(qt, unicode):
                qt = unicode(qt, "utf-8")
            if qt in dic:
                if dic[qt] > maxNTScore:
                    maxNTScore = dic[qt]
        ntfreq += maxNTScore

    # Loop nest 2, in the other direction...
    for qt in q:
        if not isinstance(qt, unicode):
            qt = unicode(qt, "utf-8")

        maxQTScore = 0.0
        for ttt in t:
            if ttt in modelCache:
                dic = modelCache[ttt]
            else:
                dic = model.similarToTerm(ttt, number)
                modelCache[ttt] = dic

            if qt in dic:
                if dic[qt] > maxQTScore:
                    maxQTScore = dic[qt]
        qtfreq += maxQTScore

    # Formula
    ntfOVERns = (ntfreq / nsize) if nsize > 0 else 0.0
    qtfOVERqs = (qtfreq / qsize) if qsize > 0 else 0.0
    score = (ntfOVERns + qtfOVERqs) / 2
    return score



def matchTermsTFIDF(queryTerms, nodeTerms, nodeTFIDFDic, model, number):
    #start_time = time.time()
    # Get terms from query
    q = queryTerms
    t = nodeTerms
    qsize = len(q)
    nsize = len(t)
    ntfreq = 0.0
    qtfreq = 0.0
    #this_time = time.time()
    #print "terms calculated", str(this_time - start_time)
    global modelCache

    #Nested loop twice, once in each directions...
    #Loop nest 1...
    for ttt in t:
        if ttt in modelCache:
            dic = modelCache[ttt]
        else:
            dic = model.similarToTerm(ttt, number)
            modelCache[ttt] = dic

        #print "q: ",q
        #print "t: ",t
        #print "dic: ", dic
        #print "Press return to continue"
        #text = sys.stdin.readline()
        maxNTScore = 0.0
        for qt in q:
            if not isinstance(qt, unicode):
                qt = unicode(qt, "utf-8")
            if qt in dic:
                #print "QT:",qt
                #print "TTT:",ttt
                #print "catTFIDFDic:",catTFIDFDic
                embeddingRelevancy = dic[qt]
                termTFIDF = nodeTFIDFDic[ttt]
                combinedScore = embeddingRelevancy * termTFIDF
                if combinedScore > maxNTScore:
                    maxNTScore = combinedScore
        ntfreq += maxNTScore

    # Loop nest 2, in the other direction...
    for qt in q:
        if not isinstance(qt, unicode):
            qt = unicode(qt, "utf-8")

        maxQTScore = 0.0
        for ttt in t:
            if ttt in modelCache:
                dic = modelCache[ttt]
            else:
                dic = model.similarToTerm(ttt, number)
                modelCache[ttt] = dic

            if qt in dic:
                embeddingRelevancy = dic[qt]
                termTFIDF = nodeTFIDFDic[ttt]
                combinedScore = embeddingRelevancy * termTFIDF
                if combinedScore > maxQTScore:
                    maxQTScore = combinedScore
        qtfreq += maxQTScore

    # Formula
    ntfOVERns = (ntfreq / nsize) if nsize > 0 else 0.0
    qtfOVERqs = (qtfreq / qsize) if qsize > 0 else 0.0
    score = (ntfOVERns + qtfOVERqs) / 2
    return score


def __weightedSize(entitySet, distance=5):
    total = 0.0
    #print list(entitySet)
    for item in entitySet:
        #print item
        if int(entitySet[item]) <= distance:
            total += 1.0 / float(entitySet[item])
    return total

def __intersection(qents,nents, distance=5):
    size = 0.0
    for qek in qents:
        for nek in nents:
            if (qek == nek) and (int(qents[qek]) <= distance) and (int(nents[nek]) <= distance):
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
        #print "qentity, score: ",qentity, qscore
        for nek in nodeEntities:
            nentity = nodeEntities[nek]
            nscore = float(nentity['score'])
            #print "Nentity, score: ", nentity, nscore
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

            #We don't necessarily need to recalculate the weighted sizes of these subject collections over and over again. Cache these values.
            if 'subjWS' in qentity:
                wQS = qentity['subjWS']
            else:
                wQS = __weightedSize(qentity[key])
                qentity['subjWS'] = wQS

            if 'subjWS' in nentity:
                wNS = nentity['subjWS']
            else:
                wNS = __weightedSize(nentity[key])
                nentity['subjWS'] = wNS


            if wQS > 0:
                wMwQS = wM/wQS
            else:
                wMwQS = 0
            if wNS > 0:
                wMwNS = wM/wNS
            else:
                wMwNS = 0
            score = ((wMwQS + wMwNS) / 2) * nscore * qscore
            #if score > 0:
                #print "Nentity, score: ", nentity, nscore
                #print "(" + str(wMwQS) + " + " + str(wMwNS) + ") / 2"

            entsScore += score

    ''' 
    Divide the total score by the total number of permutations of qentities vs nentities, to get a value out of 1.0
    '''
    perms = len(queryEntities) * len(nodeEntities)

    entsScore = (entsScore / perms) if (perms > 0) else 0
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
            #Changing this to create embeddings from full description, not local node label
            #ct = text2terms(categoryNode['label'])
            ct = text2terms(categoryNode['allDescriptions'])
            categoryNode['terms'] = ct
            #print "Node full Desc: ",categoryNode['allDescriptions']
        #return matchTerms(qt, ct, model, embeddings)
        return matchTermsTFIDF(qt, ct, categoryNode['termTFIDF'], model, embeddings)
    elif method == 'combined':
        return (matchNodes(queryNode, categoryNode, 'terms', model, embeddings) + matchNodes(queryNode, categoryNode, 'subjects', model, embeddings))/2

    else:
        raise ValueError('Unknown method: ' + method)    