import os
import csv
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import io
import sys

"""Returns a double"""
def matchTerms(query, node):
    # Get terms from query
    t = query['terms'].keys()
    if not 'terms' in node:
        return 0.0
    nsize = len(node['terms'])
    qsize = len(query['terms'])
    tfreq = 0.0
    for ttt in node['terms']:
        dic = node['terms'][ttt]
        for qt in t:
            if qt in dic:
                tfreq += dic[qt]
    
    # Formula
    score = ((tfreq / nsize) + (tfreq / qsize)) / 2
    return score