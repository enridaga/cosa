#!/usr/local/bin/python


def _test():
    import sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from cosa.search.functions import createQueryNode, matchNodes
    from cosa.graph.functions import traverse
    import pprint

    nodeA = createQueryNode('flying drone quadcopter')
    nodeB = createQueryNode('autonomous vehicle')
    #pprint.pprint (nodeB)

    result = matchNodes(nodeA,nodeB)
    print result

def _search(text):
    from cosa.search.functions import entities
    from cosa.search.DBPedia import DBPedia
    myDBPedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    entities(text, myDBPedia)
    
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