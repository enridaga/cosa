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

    #dbpedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    dbpedia = DBPedia('http://kmi-appsvr06.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    g = loadGraph(input)
    def populate(n):
        if 'label' in n:
            n['entities'] = entities(n['allDescriptions'],dbpedia)
            print n['code'], n['entities']
    traverse(g, populate)
    saveGraph(g, output)

def _fixEntities(input, output):
    from cosa.graph.functions import traverse, saveGraph, loadGraph
    from cosa.search.functions import entities
    from cosa.dbpedia.DBPedia import DBPedia
    dbpedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    g = loadGraph(input)
    def fix(n):
        if 'entities' in n:
            for resource in n['entities']:
                tempDict = {}
                for item in n['entities'][resource]['subjects']:
                    k, v = item.items()[0]
                    tempDict[k] = v
                n['entities'][resource]['subjects'] = tempDict
            print n['code']
    traverse(g, fix)
    saveGraph(g, output)

'''
#this function is incomplete but we probably don't need it for now
def _removeDupEntities(input, output):
    from cosa.graph.functions import traverse, saveGraph, loadGraph
    from cosa.search.functions import entities
    from cosa.dbpedia.DBPedia import DBPedia
    dbpedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    g = loadGraph(input)
    def removeDups(n):
        if 'entities' in n:
            entitiesLookup = {}
            for spotlightKey in n['entities']:
                for subjectKey in n['entities'][spotlightKey]['subjects']:
                    if subjectKey in entitiesLookup:
                        #we've already seen this key - check the distance value we have so far
                        if n['entities'][spotlightKey]['subjects'][subjectKey] < entitiesLookup[subjectKey]['distance']:
                            #we've found a new lower value, store this in our log and go back and remove the
                            #older entry with the higher value
                            
                            entitiesLookup[subjectKey] = n['entities'][spotlightKey]['subjects'][subjectKey]
                            seenSubjects[subjectKey] = n['entities'][spotlightKey]['subjects'][subjectKey]
                        else:
                            #the value we already have found was lower, so remove this entry
                            remove entry here..
                    else:
                        #we've not see this one before, so add it
                        entitiesLookup[subjectKey] = {'spotlight':spotlightKey, 'distance': n['entities'][spotlightKey]['subjects'][subjectKey]}
            n['entities']['subjects'] = newSubjDict
            print n['code']
    traverse(g, removeDups)
    saveGraph(g, output)
'''

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
    elif (func == 'remove-dup-entities'):
        _removeDupEntities(sys.argv[2], sys.argv[3])
    elif (func == 'fix-entities'):
        _fixEntities(sys.argv[2], sys.argv[3])
    else:
        print 'Dunno'

if __name__ == "__main__":
    main()