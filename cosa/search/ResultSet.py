class ResultSet:
    def __init__(self):
        self.results = []

    def collect(self, node):
        self.results.append(node)

    def getResults(self):
        return self.results

