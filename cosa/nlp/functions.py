import os
import csv
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import io
import sys

def text2terms(text):
    lemmatiser = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tokens_pos = pos_tag(tokens)
    keywords = []
    for token in tokens_pos:
        if len(token[0]) < 3:
            continue
        if token[1]:
           try:
               lemma = lemmatiser.lemmatize(token[0], pos=token[1][0:1].lower())
           except Exception as e:
               lemma = lemmatiser.lemmatize(token[0])
           keywords.append(enpos(token[0], token[1]))
    return keywords

def enpos(lemma, pos):
    return lemma.lower() + '[' + pos[0:1].lower() + ']'

def depos(term):
    return term[0:term.find('[')]