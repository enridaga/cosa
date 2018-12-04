import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.graph.functions import traverse, saveGraph, loadGraph
from cosa.dbpedia.DBPedia import DBPedia

# dbpedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
def entities(input, dbpedia):
    from cosa.dbpedia.DBPedia import DBPedia
    spotlight = dbpedia.spotlight(input, 0.1)
    entities = {}

    #if no entities returned (eg root node), just return empty entities dict

    for item in spotlight or []:
        entities[item] = {}
        entities[item]['score'] = spotlight[item]['score']
        entities[item]['types'] = []
        entities[item]['subjects'] = []
        dbpSubjsTypes = dbpedia.getSubjTypeURIs(item) #returns an array
        for arrayItem in dbpSubjsTypes:
            if arrayItem['type'] == 'S':
                entities[item]['subjects'].append(arrayItem['uri'])
            elif arrayItem['type'] == 'T':
                entities[item]['types'].append(arrayItem['uri'])
            else:
                pass #it wasn't a 'subject' or 'Type', something went wrong
    return entities
    

def prepareQueryNode(input):
    from cosa.dbpedia.DBPedia import DBPedia
    from cosa.nlp.functions import text2terms
    node = {}
    node['label'] = input
    node['other'] = False
    node['terms'] = {}
    node['entities'] = {}
    #Now create terms from label
    for term in text2terms(node['label']):
        node['terms'][term] = {
            term: 1.0
        }
    return node
            
def createQueryNode(input):
    from cosa.dbpedia.DBPedia import DBPedia
    from cosa.nlp.functions import text2terms
    node = prepareQueryNode(input)
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
    return node

def sortAndCut(queue,percentage):
    from operator import itemgetter
    sortedList = sorted(queue, key=itemgetter('parentScore'),reverse=True)
    newLength = int(float(len(sortedList)) * (float(percentage)/100))
    return sortedList[:newLength]

def searchGraph(input, graph):
    qNode = createQueryNode(input)
    thisQ = []
    nextQ = []
    model = Model(modelFile)
    rs = ResultSet()

    #initially populate thisQ with graph root first layer subs
    for sub in graph['subs']:
        thisQ.append(graph['subs'][sub])

    while (thisQ > 0) or (nextQ > 0):
        while thisQ > 0:
            currentNode = thisQ.pop()
            score = nodeMatch(qNode, currentNode)
            if 'parentScore' in currentNode:
                score += currentNode['parentScore']
            currentNode['score'] = score
            if isLeaf(currentNode):
                rs.collect(currentNode)
            else:
                for sub in currentNode['subs']:
                    currentNode['subs'][sub]['parentScore'] = score
                    nextQ.append(currentNode['subs'][sub])

        thisQ = sortAndCut(nextQ,50)
        nextQ = []












def addNodeToQueryGraph():
    return True

def createQueryGraph():
    return True



def testFunction():
    print ("Hello")