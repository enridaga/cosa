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

def _runTest(inputFile, graphFile):
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

    processLog = []
    output = 'output.csv'


    with open(inputFile , 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        print "Writing data to " + output
        with open(output, 'wb') as csvoutput:
            writer = csv.writer(csvoutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csvreader:
                outputRow = [None] * 7
                outputRow[0] = row[0]  # tariff code
                outputRow[1] = row[1]  # description field
                outputRow[2] = ''   # number of search results
                outputRow[3] = '-'  # position in results, if found
                outputRow[4] = ''   # sample of actual search results
                outputRow[5] = ''   # branch filter, if used
                code = _padTo10(row[0])

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
                    rs = searchGraph(textSanitized, g, 'entities', 3)
                    print '**************'
                    print code, textSanitized
                    print 'Top 10 results by normalised(by depth) score'
                    rs.printTopNScores(10);



    return True


def main():
    if len(sys.argv) == 1:
        exit(1)

    func = sys.argv[1]
    if (func == 'runtest'):
        _runTest(sys.argv[2],sys.argv[3])
    else:
        print 'Unrecognised parameter'


if __name__ == "__main__":
    main()