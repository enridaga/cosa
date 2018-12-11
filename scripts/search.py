#!/usr/local/bin/python
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.search.functions import createQueryNode, sortAndCut, searchGraph
from cosa.graph.functions import traverse, loadGraph
from cosa.search.ResultSet import ResultSet
from cosa.nlp.Model import *

def _test():
    import sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from cosa.search.functions import createQueryNode, sortAndCut, searchGraph
    from cosa.graph.functions import traverse, loadGraph

    print 'test'
    g = loadGraph('../data/graph_entities.dict')
    searchGraph('knitted jumper',g)

def _search():
    print 'Loading graph...'
    g = loadGraph('../data/graph_entities.dict')
    print 'Graph loaded.'

    print 'Loading model...'
    model = Model('/Users/jc33796/Documents/UKPostings/Data/Gutenberg2Vec/word2vec.model')
    #model = Model('/Users/ed4565/Development/led-discovery/data/analysis/gutenberg2vec/word2vec.model')
    
    print 'Model loaded.'

    while(True):
        print 'Search:'
        try:
            text = sys.stdin.readline()
            text = text.split(':')
            method = 'entities'
            if len(text) > 1:
                method = text[0]
                text = text[1]
            print 'Searching with method ' + method + '...'
            rs = ResultSet()
            if method == 'terms':
                rs = searchGraph(text, g, method, model, 50, 0)
            else:
                rs = searchGraph(text, g, method, None, 50, 0)

            #print '**************'
            #print 'Top 10 results by score'
            #rs.printTopScores(10);

            print '**************'
            print 'Top 10 results by normalised(by depth) score'
            rs.printTopNScores(10);
        except Exception as e:
            print e
            pass #print " - not found (exception)"
        except Error as r:
            print r
            pass #print " - error"
    
def main():
    if len(sys.argv) == 1:
        exit(1)
        
    func = sys.argv[1]
    if(func == 'search'):
        _search()
    else:
        _test()


if __name__ == "__main__":
    main()