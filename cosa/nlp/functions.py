import os
import csv
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import io
import sys

"""Returns an array of keywords"""
def text2terms(text):
    lemmatiser = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tokens_pos = pos_tag(tokens)
    keywords = []
    for token in tokens_pos:
        #print token
        lemma = None
        if len(token[0]) < 3:
            continue
        if token[1]:
            # print token[0]
            try:
                lemma = lemmatiser.lemmatize(token[0].lower(), pos=token[1][0:1].lower())
            except Exception as e:
                pass
        try:
            if lemma == None:
                lemma = lemmatiser.lemmatize(token[0].lower())
            keywords.append(enpos(lemma, token[1]))
        except Exception as e:
            pass
    
    #print keywords
    return keywords

def enpos(lemma, pos):
    return lemma.lower() + '[' + pos[0:1].lower() + ']'

def depos(term):
    return term[0:term.find('[')]