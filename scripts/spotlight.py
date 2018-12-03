#!/usr/local/bin/python
import pprint

def main():
    import sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    #from cosa.dbpedia.spotlight import spotlight
    from cosa.dbpedia.DBPedia import DBPedia

    myDBPedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    spotlight = myDBPedia.spotlight('Tesco Lamb Sliced Liver',0.1)

    pprint.pprint (spotlight)

    #print ('##########')
    #dbpResults = myDBPedia.dbpediaEndpointRequest('http://dbpedia.org/resource/Liver_(food)')
    #print(dbpResults)

    print ('##########')
    dbpSimplified = myDBPedia.getSubjURIs('http://dbpedia.org/resource/Tesco')
    pprint.pprint (dbpSimplified)


if __name__ == "__main__":
    main()