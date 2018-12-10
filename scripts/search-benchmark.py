#!/usr/local/bin/python
import sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.search.functions import createQueryNode, sortAndCut, searchGraph
from cosa.graph.functions import traverse, loadGraph
from cosa.search.ResultSet import ResultSet
from cosa.nlp.Model import *



def _singleSearch():
    print 'Loading graph...'
    g = loadGraph('../data/graph_entities.dict')
    print 'Graph loaded.'

    print 'Loading model...'
    # model = Model('/Users/jc33796/Documents/UKPostings/Data/Gutenberg2Vec/word2vec.model')
    print 'Model loaded.'

    while (True):
        print 'Search:'
        text = sys.stdin.readline()
        text = text.split(':')
        method = 'entities'
        if len(text) > 1:
            method = text[0]
            text = text[1]
        print 'Searching with method ' + method + '...'
        rs = ResultSet()
        if method == 'terms':
            rs = searchGraph(text, g, method, 3)
        else:
            rs = searchGraph(text, g, method, 3)

        print '**************'
        print 'Top 10 results by score'
        rs.printTopScores(10);

        print '**************'
        print 'Top 10 results by normalised(by depth) score'
        rs.printTopNScores(10);

def _needs_escaping(character):

    escape_chars = {
        '\\' : True, '+' : True, '-' : True, '!' : True,
        '(' : True, ')' : True, ':' : True, '^' : True,
        '[' : True, ']': True, '\"' : True, '{' : True,
        '}' : True, '~' : True, '*' : True, '?' : True,
        '|' : True, '&' : True, '/' : True
    }
    return escape_chars.get(character, False)

def _padTo10 (input):
    inputStr = str(input)
    if len(inputStr) < 10:
        for x in range(10 - len(inputStr)):
            inputStr = "0" + inputStr
    return inputStr

def isMatch (inputA, inputB, sigFigs):
    modifiedA = inputA[:sigFigs]
    modifiedB = inputB[:sigFigs]
    for x in range(10 - sigFigs):
        modifiedA = modifiedA + "0"
        modifiedB = modifiedB + "0"
    return (modifiedA == modifiedB)

def _runTest(inputFile, graphFile, outputFile):
    '''
    This function runs the main test that we will be using to benchmark search algorithms using
    a ground-truth input file
    :param input: the filename of the search test input file
    :param graph: a graph/dictionary to search against
    :return:
    '''
    print 'Loading graph...'
    g = loadGraph(graphFile)
    print 'Graph loaded.'
    print 'Loading model...'
    model = Model('/Users/jc33796/Documents/UKPostings/Data/Gutenberg2Vec/word2vec.model')

    processLog = []

    with open(inputFile , 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        print "Writing data to " + outputFile
        with open(outputFile, 'wb') as csvoutput:
            writer = csv.writer(csvoutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            outputHeader = [None] * 9
            outputHeader[0] = 'code'  # tariff code
            outputHeader[1] = 'description'  # description field
            outputHeader[2] = 'search results'  # number of search results
            outputHeader[3] = 'position(2)'  # position in results, if found
            outputHeader[4] = 'position(4)'  # position in results, if found
            outputHeader[5] = 'position(6)'  # position in results, if found
            outputHeader[6] = 'position(8)'  # position in results, if found
            outputHeader[7] = 'position(10)'  # position in results, if found
            outputHeader[8] = 'results sample(10)'
            writer.writerow(outputHeader)
            for row in csvreader:
                code = _padTo10(row[0])

                outputRow = [None] * 9
                outputRow[0] = code  # tariff code
                outputRow[1] = row[1]  # description field
                outputRow[2] = ''   # number of search results
                outputRow[3] = '-'  # position in results (2), if found
                outputRow[4] = '-'  # position in results (4), if found
                outputRow[5] = '-'  # position in results (6), if found
                outputRow[6] = '-'  # position in results (8), if found
                outputRow[7] = '-'  # position in results (10), if found
                outputRow[8] = '-'   # sample of actual search results

                #searching using dbpedia keywords
                textSearchTerm = row[1]
                dbpSearchTerm = row[2]
                textSanitized = ''
                dbpSanitized= ''
                # escape any difficult chars
                for character in textSearchTerm:
                    if _needs_escaping(character):
                        textSanitized += '\\%s' % character
                    else:
                        textSanitized += character

                for character in dbpSearchTerm:
                    if _needs_escaping(character):
                        dbpSanitized += '\\%s' % character
                    else:
                        dbpSanitized += character

                codeTerm = str(code) + '-' + row[1]

                # Check if we've already done this code-term combo (and whether we're processing duplicates)
                if codeTerm in processLog:
                    #no need to run this search again
                    pass
                else:
                    processLog.append(codeTerm)

                    # Do ES search...
                    #For dbpedia URIs, enclose each one in quotes
                    textSanitized = textSanitized.strip()
                    dbpSanitized = dbpSanitized.strip()

                    dbpSanitized = '"' + '" "'.join(dbpSanitized.split(' ')) + '"'


                    '''
                    #####################
                    Start searching here...
                    #####################
                    '''
                    rs = ResultSet()
                    #model = None
                    rs = searchGraph(textSanitized, g, 'terms', model, 50, 1)
                    print '**************'
                    print code, textSanitized
                    #print 'Top 10 results by normalised(by depth) score'
                    #rs.printTopNScores(10);
                    sortedRes = rs.sortByNScore()

                    # Generate a string of first 10 results
                    top10String = ''
                    counter = 0
                    for item in sortedRes:
                        counter += 1
                        top10String = top10String + item['code'] + ';'
                        if counter >= 10:
                            break

                    topPosition = {}
                    for i in (2, 4, 6, 8, 10):
                        topPosition[i] = 0

                        for item in sortedRes:
                            if isMatch(code,item['code'],i) and (((item['position']) < topPosition[i]) or (topPosition[i] == 0)):
                                topPosition[i] = item['position']
                                #print 'HIT at ',i,': ', topPosition[i]
                    outputRow[2] = len(sortedRes)
                    outputRow[3] = topPosition[2] if topPosition[2] > 0 else ''
                    outputRow[4] = topPosition[4] if topPosition[4] > 0 else ''
                    outputRow[5] = topPosition[6] if topPosition[6] > 0 else ''
                    outputRow[6] = topPosition[8] if topPosition[8] > 0 else ''
                    outputRow[7] = topPosition[10] if topPosition[10] > 0 else ''
                    #outputRow[8] = unicode(top10String, 'utf-8')
                    outputRow[8] = top10String.encode('utf-8')
                    writer.writerow(outputRow)
    return True


def main():
    if len(sys.argv) == 1:
        exit(1)

    func = sys.argv[1]
    if (func == 'runtest'):
        _runTest(sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        print 'Unrecognised parameter'


if __name__ == "__main__":
    main()