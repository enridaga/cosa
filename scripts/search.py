#!/usr/local/bin/python
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.search.functions import createQueryNode, sortAndCut, searchGraph, searchGraphCombined
from cosa.graph.functions import traverse, loadGraph
from cosa.search.ResultSet import ResultSet
from cosa.nlp.Model import *

def _test():
    import sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from cosa.search.functions import createQueryNode, sortAndCut, searchGraph, searchGraphCombined
    from cosa.graph.functions import traverse, loadGraph

    print 'test'
    g = loadGraph('./graph_entities_terms.dict')
    searchGraph('knitted jumper',g)

def _search():
    print 'Loading graph...'
    g = loadGraph('./graph_entities_terms.dict')
    print 'Graph loaded.'

    print 'Loading model...'
    model = Model('/Users/jc33796/Documents/UKPostings/Data/Gutenberg2Vec/word2vec.model')
    #model = Model('/Users/ed4565/Development/led-discovery/data/analysis/gutenberg2vec/word2vec.model')
    #model = None
    print 'Model loaded.'

    while(True):
        print 'Search:'
        try:
            text = sys.stdin.readline()
            text = text.split(':')
            method = 'terms'
            if len(text) > 1:
                method = text[0]
                text = text[1]
            print 'Searching with method ' + method + '...'
            rs = ResultSet()
            if method == 'combinedold':
                rs = searchGraphCombined(text, g, method, model, 100, 2)

                print '**************'
                print 'Top 10 COMBINED results by normalised(by depth) score'
                rs.printTopNScoresCombined(10);
                print 'NOW MERGE...'
                rs.sortByTwoScores('nScoreT', 'nScoreS', 10)

            else:
                rs = searchGraph(text, g, method, model, 100, 0)

                print '**************'
                print 'Top 10 results by normalised(by depth) score'
                rs.printTopNScores(10);


        except Exception as e:
            print e
            pass #print " - not found (exception)"
        except Error as r:
            print r
            pass #print " - error"


def _embeddings():
    print 'Loading model...'
    model = Model('/Users/jc33796/Documents/UKPostings/Data/Gutenberg2Vec/word2vec.model')
    # model = Model('/Users/ed4565/Development/led-discovery/data/analysis/gutenberg2vec/word2vec.model')
    print 'Model loaded.'

    while (True):
        print 'Retrieve embeddings:'
        try:
            text = sys.stdin.readline().split('\n')[0]
            dic = model.similarToTerm(text,100)
            print dic


        except Exception as e:
            print e
            pass  # print " - not found (exception)"
        except Error as r:
            print r
            pass  # print " - error"


def main():
    if len(sys.argv) == 1:
        exit(1)
        
    func = sys.argv[1]
    if(func == 'search'):
        _search()
    elif(func == 'embeddings'):
        _embeddings()
    else:
        _test()


if __name__ == "__main__":
    main()