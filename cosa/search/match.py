import os
import csv
from cosa.nlp.functions import *
import io
import sys

"""Returns a double"""
def matchTerms(queryLabel, nodeLabel, model):
    # Get terms from query
    q = text2terms (queryLabel)
    t = text2terms (nodeLabel)
    qsize = len(q)
    nsize = len(t)
    tfreq = 0.0
    
    for ttt in t:
        dic = model.similarToTerm(ttt, 100000)
        for qt in q:
            if not isinstance(qt, unicode):
                qt = unicode(qt, "utf-8")
            if qt in dic:
                tfreq += dic[qt]
    
    # Formula
    score = ((tfreq / nsize) + (tfreq / qsize)) / 2
    return score