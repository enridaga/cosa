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
    from cosa.graph.functions import traverse, saveGraph
    m = Model(file)
    g = loadGraph(inp)
    def populate(n):
        terms = text2terms()
        n['terms'] = {}
        for t in terms:
            sim = m.similarToTerm(t, 100)
            n['terms'][t] = sim
        
    traverse(g, populate)
    saveGraph(g, out)
    
    
def main():
    if len(sys.argv) == 1:
        exit(1)
        
    func = sys.argv[1]
    if(func == 'csv2graph'):
        _csv2graph(sys.argv[2], sys.argv[3])
    if(func == 'embeddings'):
        _embeddings(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print 'Dunno'

if __name__ == "__main__":
    main()