import sys
import numpy as np
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.graph.functions import traverse, saveGraph, loadGraph
from cosa.dbpedia.DBPedia import DBPedia
from cosa.search.match import matchNodes
from cosa.search.ResultSet import ResultSet

# dbpedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
def entities(input, dbpedia, confidence = 0.1):
    from cosa.dbpedia.DBPedia import DBPedia
    spotlight = dbpedia.spotlight(input, confidence)
    entities = {}

    #if no entities returned (eg root node), just return empty entities dict
    for item in spotlight or []:
        entities[item] = {}
        entities[item]['score'] = spotlight[item]['score']
        entities[item]['types'] = {}
        entities[item]['subjects'] = {}
        dbpSubjsTypes = dbpedia.getSubjURIs(item) #returns an array
        for arrayItem in dbpSubjsTypes:
            if arrayItem['type'] == 'S':
                entities['entities'][item]['subjects'][arrayItem['uri']] = arrayItem['distance']
            elif arrayItem['type'] == 'T':
                entities['entities'][item]['types'][arrayItem['uri']] = arrayItem['distance']
            else:
                pass #it wasn't a 'subject' or 'Type', something went wrong
            
        #entities[item]['types'] = list(set(entities[item]['types']))
        #entities[item]['subjects'] = list(set(entities[item]['subjects']))

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

dbpCache = {}
spotlightCache = {}

def createQueryNode(input):
    from cosa.dbpedia.DBPedia import DBPedia
    from cosa.nlp.functions import text2terms
    global dbpCache
    global spotlightCache
    node = prepareQueryNode(input)
    myDBPedia = DBPedia('http://anne.kmi.open.ac.uk/rest/annotate', 'http://dbpedia.org/sparql')
    if input in spotlightCache:
        spotlight = spotlightCache[input]
    else:
        spotlight = myDBPedia.spotlight(input, 0.1)
        spotlightCache[input] = spotlight
    global dbpCache
    if spotlight:
        for item in spotlight:
            node['entities'][item] = {}
            node['entities'][item]['score'] = spotlight[item]['score']
            node['entities'][item]['types'] = {}
            node['entities'][item]['subjects'] = {}
            if item in dbpCache:
                dbpSubjsTypes = dbpCache[item]
            else:
                dbpSubjsTypes = myDBPedia.getSubjURIs(item) #returns an array of dictionaries {'uri':<uri>,'type':<type>,{distance':<distance>}
                dbpCache[item] = dbpSubjsTypes
            for arrayItem in dbpSubjsTypes:
                if arrayItem['type'] == 'S':
                    #singleItem = {}
                    #singleItem[arrayItem['uri']] = arrayItem['distance']
                    #node['entities'][item]['subjects'].append(singleItem)
                    node['entities'][item]['subjects'][arrayItem['uri']] = arrayItem['distance']
                elif arrayItem['type'] == 'T':
                    #singleItem = {}
                    #singleItem[arrayItem['uri']] = arrayItem['distance']
                    #node['entities'][item]['types'].append(singleItem)
                    node['entities'][item]['types'][arrayItem['uri']] = arrayItem['distance']
                else:
                    pass #it wasn't a 'subject' or 'Type', something went wrong
            #SELECT DISTINCT should render the following redundant
            #node['entities'][item]['subjects'] = list(set(node['entities'][item]['subjects']))
    return node

def sortAndCut(queue,percentage,field):
    from operator import itemgetter
    #sortedList = sorted(queue, key=itemgetter('parentScore'),reverse=True)
    sortedList = sorted(queue, key=itemgetter(field),reverse=True)
    newLength = int(float(len(sortedList)) * (float(percentage)/100))
    return sortedList[:newLength]

def sortAndCutOnScore(queue,percentage,field):
    from operator import itemgetter
    sortedList = sorted(queue, key=itemgetter(field),reverse=True)
    topScore = float(sortedList[0][field])
    bottomScore = float(sortedList[len(sortedList)-1][field])

    #calc SD and mean
    scoresList = []
    for item in sortedList:
        scoresList.append(item[field])
    SD = np.std(scoresList)
    mean = np.mean(scoresList)

    cutScore = topScore - ((topScore - bottomScore) * (float(percentage)/100))
    print ''
    print 'Processing:',field
    print 'Top score:',topScore
    print 'Bottom score:',bottomScore
    print 'SD:',SD
    print 'Mean:',mean
    print 'Cut score:',cutScore
    index = 0
    for item in sortedList:
        index += 1
        if float(item[field]) < cutScore:
            break
    #newLength = int(float(len(sortedList)) * (float(percentage)/100))
    newLength = index
    print 'Cut index:',index
    return sortedList[:newLength]

def isLeaf(node):
    if ('sub' in node):
        if len(node['sub']) > 0:
            return False
        else:
            return True
    else:
        return True

def searchGraph(input, graph, method, model, cutPercent, stop = 0):
    qNode = createQueryNode(unicode(input, 'utf-8'))
    thisQ = []
    thisQScored = []
    thisQScoredSorted = []
    nextQ = []
    rs = ResultSet()
    currentDepth = 1
    #score = 0.0

    #initially populate thisQ with graph root first layer subs
    for sub in graph['sub']:
        graph['sub'][sub]['depth'] = currentDepth
        thisQ.append(graph['sub'][sub])

    while thisQ or nextQ:
        print ''
        sys.stdout.write('Processing queue. Depth: ' + str(currentDepth) + ' ')
        while thisQ:
            sys.stdout.write('.')
            sys.stdout.flush()
            currentNode = thisQ.pop()
            currentNode['localScore'] = matchNodes(qNode, currentNode, method, model)
            #currentNode['localScore'] = score
            if 'parentScore' in currentNode:
                currentNode['score'] = currentNode['parentScore'] + currentNode['localScore']
            else:
                currentNode['parentScore'] = 0.0
                currentNode['score'] = currentNode['parentScore'] + currentNode['localScore']
            #currentNode['score'] = score
            thisQScored.append(currentNode)
        #thisQScoredSorted = sortAndCut(thisQScored,cutPercent,'score')
        thisQScoredSorted = sortAndCutOnScore(thisQScored,cutPercent,'score')
        while thisQScoredSorted:
            currentNode = thisQScoredSorted.pop()
            #if isLeaf(currentNode) or (currentDepth == stop):
            if isLeaf(currentNode) or (str(currentNode['row']['Hier.Pos.']) == str(stop)):
                currentNode['nScore'] = currentNode['score'] / currentDepth
                print 'collecting ',currentNode['code'], currentNode['localScore'], currentNode['score'], currentNode['nScore'], currentDepth
                #don't collect items with zero score...
                if currentNode['nScore'] > 0:
                    rs.collect(currentNode)
            else:
                # push all subs to the next queue
                for sub in currentNode['sub']:
                    currentNode['sub'][sub]['parentScore'] = currentNode['parentScore'] + currentNode['localScore']
                    currentNode['sub'][sub]['depth'] = currentDepth + 1
                    nextQ.append(currentNode['sub'][sub])
        thisQ = list(nextQ)
        thisQScored = []
        nextQ = []
        currentDepth += 1
    print 'Items collected: ',rs.length()
    return rs

'''
This function largely replicates that of searchGraph(), but looks at matching each node
twice - once for the embeddings terms and again for the dbpedia subjects. At each stage, one
version of thisQ is maintained (the list of nodes to be processed), but the results are sorted and cut twice
into two lists (one for each scoring method), before being merged and pushed into nextQ 
'''
def searchGraphCombined(input, graph, method, model, cutPercent, stop = 0):
    qNode = createQueryNode(unicode(input, 'utf-8'))
    thisQ = []
    thisQScored = []
    thisQScoredSortedT = []
    thisQScoredSortedS = []
    nextQ = []
    rs = ResultSet()
    currentDepth = 1
    #score = 0.0

    #initially populate thisQ with graph root first layer subs
    for sub in graph['sub']:
        graph['sub'][sub]['depth'] = currentDepth
        thisQ.append(graph['sub'][sub])

    while thisQ or nextQ:
        print ''
        sys.stdout.write('Processing queue. Depth: ' + str(currentDepth) + ' ')
        while thisQ:
            sys.stdout.write('.')
            sys.stdout.flush()
            currentNode = thisQ.pop()
            currentNode['localScoreT'] = matchNodes(qNode, currentNode, 'terms', model)
            currentNode['localScoreS'] = matchNodes(qNode, currentNode, 'subjects', model)
            if 'parentScoreT' in currentNode:
                currentNode['scoreT'] = currentNode['parentScoreT'] + currentNode['localScoreT']
            else:
                currentNode['parentScoreT'] = 0.0
                currentNode['scoreT'] = currentNode['parentScoreT'] + currentNode['localScoreT']

            if 'parentScoreS' in currentNode:
                currentNode['scoreS'] = currentNode['parentScoreS'] + currentNode['localScoreS']
            else:
                currentNode['parentScoreS'] = 0.0
                currentNode['scoreS'] = currentNode['parentScoreS'] + currentNode['localScoreS']

            thisQScored.append(currentNode)


        thisQScoredSortedT = sortAndCutOnScore(thisQScored,cutPercent,'scoreT')
        thisQScoredSortedS = sortAndCutOnScore(thisQScored, cutPercent, 'scoreS')

        mergedList = thisQScoredSortedT + thisQScoredSortedS
        mergedListUnique = []
        for item in mergedList:
            if item in mergedListUnique:
                pass
            else:
                mergedListUnique.append(item)

        while mergedListUnique:
            currentNode = mergedListUnique.pop()
            #if isLeaf(currentNode) or (currentDepth == stop):
            if isLeaf(currentNode) or (str(currentNode['row']['Hier.Pos.']) == str(stop)):
                currentNode['nScoreT'] = currentNode['scoreT'] / currentDepth
                currentNode['nScoreS'] = currentNode['scoreS'] / currentDepth
                print 'collecting ',currentNode['code'], currentNode['nScoreT'], currentNode['nScoreS'], currentDepth
                #don't collect items with zero score...
                if (currentNode['nScoreS'] > 0) or (currentNode['nScoreT'] > 0):
                    rs.collect(currentNode)
            else:
                # push all subs to the next queue
                for sub in currentNode['sub']:
                    currentNode['sub'][sub]['parentScoreT'] = currentNode['parentScoreT'] + currentNode['localScoreT']
                    currentNode['sub'][sub]['parentScoreS'] = currentNode['parentScoreS'] + currentNode['localScoreS']
                    currentNode['sub'][sub]['depth'] = currentDepth + 1
                    nextQ.append(currentNode['sub'][sub])
        thisQ = list(nextQ)
        thisQScored = []
        nextQ = []
        currentDepth += 1
    print 'Items collected: ',rs.length()
    return rs