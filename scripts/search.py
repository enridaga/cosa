#!/usr/local/bin/python
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.search.functions import createQueryNode, sortAndCut, searchGraph
from cosa.graph.functions import traverse, loadGraph
from cosa.search.ResultSet import ResultSet

def _test():
    import sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from cosa.search.functions import createQueryNode, sortAndCut, searchGraph
    from cosa.graph.functions import traverse, loadGraph

    print 'test'
    g = loadGraph('../data/graph_entities.dict')
    searchGraph('knitted jumper',g)






def _search(text):
    print 'Loading graph...'
    g = loadGraph('../data/graph_entities.dict')
    print 'Graph loaded.'
    rs = ResultSet()
    rs = searchGraph(text, g)

    print '**************'
    print 'Top 10 results by score'
    rs.printTopScores(10);

    print '**************'
    print 'Top 10 results by normalised(by depth) score'
    rs.printTopNScores(10);

    
def main():
    if len(sys.argv) == 1:
        exit(1)
        
    func = sys.argv[1]
    if(func == 'search'):
        _search(sys.argv[2])
    else:
        _test()


if __name__ == "__main__":
    main()