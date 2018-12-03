#!/usr/local/bin/python
import pprint

def main():
    import sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from cosa.dbpedia.DBPedia import DBPedia

    myDBPedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    spotlight = myDBPedia.spotlight('Drone',0.1)

    pprint.pprint (spotlight)

    #print ('##########')
    #dbpResults = myDBPedia.dbpediaEndpointRequest('http://dbpedia.org/resource/Liver_(food)')
    #print(dbpResults)

    print ('##########')
    dbpSimplified = myDBPedia.getSubjTypeURIs('http://dbpedia.org/resource/Unmanned_aerial_vehicle')
    pprint.pprint (dbpSimplified)


if __name__ == "__main__":
    main()