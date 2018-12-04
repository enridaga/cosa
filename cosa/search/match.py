import os
import csv
from cosa.nlp.functions import *
import io
import sys
import time

"""Returns a double"""
def matchTerms(queryLabel, nodeLabel, model, number = 1000):
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
