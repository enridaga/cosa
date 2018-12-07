from operator import itemgetter

class ResultSet:
    def __init__(self):
        self.results = []

    def collect(self, node):
        self.results.append(node)

    def getResults(self):
        return self.results

    def length(self):
        return len(self.results)

    def printTopScores(self, top=0):
        sortedList = sorted(self.results, key=itemgetter('score'), reverse=True)
        if top == 0:
            top = len(self.results)
        for item in sortedList[:top]:
            print item['code'], item['score'], item['depth'], item['label']
        return True

    def printTopNScores(self, top=0):
        sortedList = sorted(self.results, key=itemgetter('nScore'), reverse=True)
        if top == 0:
            top = len(self.results)
        for item in sortedList[:top]:
            print item['code'], item['nScore'], item['depth'], item['label']
        return True

    def getResultsCodesList(self, top=0):
        sortedList = sorted(self.results, key=itemgetter('nScore'), reverse=True)
        returnList = []
        if top == 0:
            top = len(self.results)
        for item in sortedList[:top]:
            returnList.append(item['code'])
        return returnList

    def sortByNScore(self, top=0):
        sortedList = sorted(self.results, key=itemgetter('nScore'), reverse=True)
        position = 1
        if top == 0:
            top = len(self.results)
        for item in sortedList[:top]:
            item['position'] = position
            position += 1
        return sortedList