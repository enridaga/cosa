#!/usr/local/bin/python
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

def _csv2graph(csv, out):
    from cosa.graph.functions import csv2graph
    csv2graph(csv, out)

def _embeddings(file, inp, out):
    from cosa.nlp.functions import text2terms, enpos, depos
    from cosa.nlp.Model import Model
    from cosa.graph.functions import traverse, saveGraph, loadGraph
    m = Model(file)
    g = loadGraph(inp)
    def populate(n):
        if 'label' in n:
            terms = text2terms(n['label'])
            n['terms'] = {}
            for t in terms:
                sim = m.similarToTerm(t, 100)
                n['terms'][t] = sim

    traverse(g, populate)
    saveGraph(g, out)

def _dbpedia(input, output):
    from cosa.graph.functions import traverse, saveGraph, loadGraph
    from cosa.search.functions import entities
    from cosa.dbpedia.DBPedia import DBPedia
    dbpedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    g = loadGraph(input)
    def populate(n):
        if 'label' in n:
            n['entities'] = entities(n['label'],dbpedia)
            print n['label']

    traverse(g, populate)
    saveGraph(g, out)
        
    
def browse(input):
    from cosa.graph.functions import loadGraph
    g = loadGraph(input)
    def _show(n):
        if 'code' in n:
            print n['code'], ':', n['label']
        if 'sub' in n:
            for s in n['sub']:
                print ' - ', s, ': ', n['sub'][s]['label']

    _show(g)    
    while(True):
        line = sys.stdin.readline().strip()
        if line == '':
            exit(0)
        else:
            if line in g['sub']:
                _show(g['sub'][line])
                g = g['sub'][line]
            else:
                print 'Not Found'
    
def main():
    if len(sys.argv) == 1:
        exit(1)
        
    func = sys.argv[1]
    if(func == 'csv2graph'):
        _csv2graph(sys.argv[2], sys.argv[3])
    elif(func == 'populate-terms'):
        _embeddings(sys.argv[2], sys.argv[3], sys.argv[4])
    elif(func == 'populate-entities'):
        _dbpedia(sys.argv[2], sys.argv[3])
    elif(func == 'browse'):
        browse(sys.argv[2])
    else:
        print 'Dunno'

if __name__ == "__main__":
    main()