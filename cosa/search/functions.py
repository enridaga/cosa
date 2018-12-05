import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.graph.functions import traverse, saveGraph, loadGraph
from cosa.dbpedia.DBPedia import DBPedia
from cosa.search.match import matchNodes
from cosa.search.ResultSet import ResultSet

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

def isLeaf(node):
    if ('sub' in node):
        if len(node['sub']) > 0:
            return False
        else:
            return True
    else:
        return True

def searchGraph(input, graph, method, model, stop = 0):
    qNode = createQueryNode(input)
    thisQ = []
    nextQ = []
    #model = Model(modelFile)
    rs = ResultSet()
    currentDepth = 1

    #initially populate thisQ with graph root first layer subs
    for sub in graph['sub']:
        graph['sub'][sub]['depth'] = currentDepth
        thisQ.append(graph['sub'][sub])

    while thisQ or nextQ:
        #print 'Processing queue. Depth: ', currentDepth
        while thisQ:
            currentNode = thisQ.pop()
            score = matchNodes(qNode, currentNode, method, model)
            if 'parentScore' in currentNode:
                score += currentNode['parentScore']
            currentNode['score'] = score
            if isLeaf(currentNode) or (currentDepth == stop):
                currentNode['nScore'] = currentNode['score'] / currentDepth
                #print 'collecting ',currentNode['code'], currentNode['score'], currentNode['nScore'], currentDepth
                rs.collect(currentNode)
            else:
                # push all subs to the next queue
                for sub in currentNode['sub']:
                    currentNode['sub'][sub]['parentScore'] = score
                    currentNode['sub'][sub]['depth'] = currentDepth + 1
                    nextQ.append(currentNode['sub'][sub])


        thisQ = sortAndCut(nextQ,50)
        nextQ = []
        currentDepth += 1
    print 'Items collected: ',rs.length()
    return rs











def addNodeToQueryGraph():
    return True

def createQueryGraph():
    return True



def testFunction():
    print ("Hello")