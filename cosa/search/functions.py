# dbpedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
def entities(input, dbpedia):
    spotlight = dbpedia.spotlight(input, 0.1)
    entities = {}
    for item in spotlight:
        entities[item] = {}
        entities[item]['score'] = spotlight[item]['score']
        entities['types'] = []
        entities['subjects'] = []
        dbpSubjsTypes = dbedia.getSubjTypeURIs(item) #returns an array
        for arrayItem in dbpSubjsTypes:
            if arrayItem['type'] == 'S':
                entities[item]['subjects'].append(arrayItem['uri'])
            elif arrayItem['type'] == 'T':
                entities[item]['types'].append(arrayItem['uri'])
            else:
                pass #it wasn't a 'subject' or 'Type', something went wrong
    return entities
    
    
def createQueryNode(input):
    import sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from cosa.dbpedia.DBPedia import DBPedia
    from cosa.nlp.functions import text2terms
    node = {}
    node['label'] = input
    node['other'] = False
    node['terms'] = {}
    node['entities'] = {}
    myDBPedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    spotlight = myDBPedia.spotlight(input, 0.1)
    for item in spotlight:
        node['entities'][item] = {}
        node['entities'][item]['score'] = spotlight[item]['score']
        node['entities'][item]['types'] = []
        node['entities'][item]['subjects'] = []
        dbpSubjsTypes = myDBPedia.getSubjTypeURIs(item) #returns an array
        for arrayItem in dbpSubjsTypes:
            if arrayItem['type'] == 'S':
                node['entities'][item]['subjects'].append(arrayItem['uri'])
            elif arrayItem['type'] == 'T':
                node['entities'][item]['types'].append(arrayItem['uri'])
            else:
                pass #it wasn't a 'subject' or 'Type', something went wrong

    #Now create terms from label
    for term in text2terms(node['label']):
        node['terms'][term] = {
            'term': term,
            'score': 1.0
        }

    return node

def addNodeToQueryGraph():
    return True

def createQueryGraph():
    return True

def matchNodes(queryNode, nodeInGraph):
    #Do the magic scoring here...
    return True



def testFunction():
    print ("Hello")