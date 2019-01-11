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

    def printTopNScoresCombined(self, top=0):
        sortedListT = sorted(self.results, key=itemgetter('nScoreT'), reverse=True)
        sortedListS = sorted(self.results, key=itemgetter('nScoreS'), reverse=True)

        if top == 0:
            top = len(self.results)
        print 'TERMS:'
        for item in sortedListT[:top]:
            print item['code'], item['nScoreT'], item['depth'], item['label']
        print 'SUBJECTS:'
        for item in sortedListS[:top]:
            print item['code'], item['nScoreS'], item['depth'], item['label']
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

    def removeFromList(self, field, value, L):
        for i in range(0,len(L)):
            if L[i][field] == value:
                L.pop(i)
                break

    def sortByTwoScores(self, fieldA, fieldB, top=0):
        sortedListA = sorted(self.results, key=itemgetter(fieldA), reverse=True)
        sortedListB = sorted(self.results, key=itemgetter(fieldB), reverse=True)
        sortedList = []
        while sortedListA or sortedListB:
            if sortedListA:
                tempItem = sortedListA.pop(0)
                sortedList.append(tempItem)
                self.removeFromList('code', tempItem['code'],sortedListB)
            if sortedListB:
                tempItem = sortedListB.pop(0)
                sortedList.append(tempItem)
                self.removeFromList('code', tempItem['code'],sortedListA)
        position = 1
        for item in sortedList:
            item['position'] = position
            position += 1
        if top == 0:
            top = len(sortedList)
        #for item in sortedList[:top]:
            #print item['code'], item['depth'], item['label']
        return sortedList

    def sortAndBlendTwoScores(self, fieldA, fieldB, top=0):
        maxA = 0.0
        maxB = 0.0
        #first loop through and get max values for scores A and B
        for item in self.results:
            if item[fieldA] > maxA:
                maxA = item[fieldA]
            if item[fieldB] > maxB:
                maxB = item[fieldB]

        for item in self.results:
            adjustedA = (item[fieldA] / maxA) if maxA > 0.0 else 0
            adjustedB = (item[fieldB] / maxB) if maxB > 0.0 else 0
            item['adjustedAverage'] = (adjustedA + adjustedB) / 2

        sortedList = sorted(self.results, key=itemgetter('adjustedAverage'), reverse=True)

        position = 1
        for item in sortedList:
            item['position'] = position
            position += 1
        if top == 0:
            top = len(sortedList)
        # for item in sortedList[:top]:
        # print item['code'], item['depth'], item['label']
        return sortedList
