#!/usr/local/bin/python

def main():
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



if __name__ == "__main__":
    main()