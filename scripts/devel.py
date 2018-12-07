#!/usr/local/bin/python
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.graph.functions import loadGraph, lookup
import pprint
from cosa.dbpedia.DBPedia import DBPedia
from cosa.search.functions import *

def _dataset(outputFile):
    from cosa.data.functions import dataset
    dataset(outputFile)

def __printNode(n):
    if 'code' in n:
        print('code: ' + n['code'])
    if 'label' in n:
        print('label: ' + n['label']) 
    print('entities: ')
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(n['entities'])
    
def _showNode(code):
    print 'Loading graph...'
    g = loadGraph('../data/graph_entities.dict')
    print 'Graph loaded.'
    def showOn(n):
        if 'code' in n and n['code'] == __showNode_code:
            __printNode(n)
            return False
        else:
            return True
    global __showNode_code
    __showNode_code = code
    lookup(g, showOn)

def _showEntities(text, score = 0.1):
    node = {}
    myDBPedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    #spotlight = myDBPedia.spotlight(input, 0.1)
    ents = createQueryNode(text)
    node['label'] = text
    node['entities'] = ents
    __printNode(node)

def _help():
    print 'Usage: '
    print ' ./devel.py dataset <saveToFile>'

def main():
    func = sys.argv[1];
    
    if func == 'dataset':
        _dataset(sys.argv[2]);
    elif func == 'show-node':
        _showNode(sys.argv[2])
    elif func == 'show-entities':
        _showEntities(sys.argv[2], sys.argv[3])
    
if __name__ == "__main__":
    main()