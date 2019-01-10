import requests
import time


class DBPedia:
    def loadCaches(self):
        f = open(self.spotlightCacheFile, 'r')
        data = f.read()
        f.close()
        self.spotlightCache = eval(data)

        f = open(self.subjectsCacheFile, 'r')
        data = f.read()
        f.close()
        self.subjectsCache = eval(data)

    def saveCaches(self):
        f = open(self.spotlightCacheFile, 'w')
        f.write(str(self.spotlightCache))
        f.close()

        f = open(self.subjectsCacheFile, 'w')
        f.write(str(self.subjectsCache))
        f.close()

    def __init__(self, spotlightEndpoint, dbpediaEndpoint):
        self.spotlightEndpoint = spotlightEndpoint
        self.dbpediaEndpoint = dbpediaEndpoint

        self.spotlightCacheFile = '../data/spotlightCache.dict'
        self.subjectsCacheFile = '../data/subjectsCache.dict'

        #self.loadCaches()
        self.spotlightCache = {}
        self.subjectsCache = {}
        #self.saveCaches()



    def spotlight(self, searchText, confidence):
        url = self.spotlightEndpoint
        # confidence = 0.3
        headers = {'Accept': 'application/json'}
        params = {'text': searchText.lower(), 'confidence': confidence}  # requests lib auto url-encodes this for us
        resp = requests.get(url=url, params=params, headers=headers)

        if 'Resources' in resp.json():
            # print resp.json()
            returnObj = {}
            for item in resp.json()['Resources']:
                singleResource = {}
                singleResource['score'] = item['@similarityScore']
                singleResource['offset'] = item['@offset']
                singleResource['surfaceForm'] = item['@surfaceForm']
                returnObj[item['@URI']] = singleResource

            return returnObj

        '''
        else:
            confidence = 0.2
            params = {'text': searchText.lower(), 'confidence': confidence}  # requests lib auto url-encodes this for us
            resp = requests.get(url=url, params=params, headers=headers)
            if 'Resources' in resp.json():
                #print resp.json()
                return resp.json()  # parse the JSON and return as a Python dict.
            else:
                confidence = 0.1
                params = {'text': searchText.lower(),
                          'confidence': confidence}  # requests lib auto url-encodes this for us
                resp = requests.get(url=url, params=params, headers=headers)
                #print resp.json()
                return resp.json()  # parse the JSON and return as a Python dict.
        '''

    def dbpediaEndpointRequest(self, query):
        url = self.dbpediaEndpoint
        headers = {'Accept': 'application/json'}
        params = {'query': query}
        try:
            resp = requests.get(url=url, params=params, headers=headers)
        except:
            print 'HTTP call failed, waiting 5 seconds...'
            time.sleep(5)
            resp = requests.get(url=url, params=params, headers=headers)
        return resp.json()  # parse the JSON and return as a Python dict.


    # Does a full request and returns the raw result
    def dbpediaRequestEntities(self, inputURI):
        sparqlQuery = ' \
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> \
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \
    PREFIX dct: <http://purl.org/dc/terms/> \
    SELECT distinct ?obj ?T ?L WHERE { \
      { \
      <' + inputURI + '> dct:subject ?obj . \
        bind("S" as ?T) \
        bind("1" as ?L) \
      } UNION { \
      <' + inputURI + '> dct:subject/skos:broader ?obj . \
        bind("S" as ?T) \
        bind("2" as ?L) \
      } UNION { \
      <' + inputURI + '> dct:subject/skos:broader/skos:broader ?obj . \
        bind("S" as ?T) \
        bind("3" as ?L) \
      } UNION { \
      <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something . \
        ?something dct:subject ?obj . \
        bind("S" as ?T) \
        bind("1" as ?L) \
      } UNION { \
      <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something . \
        ?something dct:subject/skos:broader ?obj . \
        bind("S" as ?T) \
        bind("2" as ?L) \
      } UNION { \
      <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something .  \
        ?something dct:subject/skos:broader/skos:broader ?obj . \
        bind("S" as ?T) \
        bind("3" as ?L) \
      } \
    }'
        return self.dbpediaEndpointRequest(sparqlQuery)


    # just get the Subject URIs
    def getSubjURIs(self, inputURI):
        returnArray = []
        if inputURI in self.subjectsCache:
            returnArray = self.subjectsCache[inputURI]
        else:
            fullResponse = self.dbpediaRequestEntities(inputURI)
            try:
                bindings = fullResponse['results']['bindings']
                for binding in bindings:
                    singleItem = {}
                    singleItem['uri'] = binding['obj']['value']
                    singleItem['type'] = binding['T']['value']
                    singleItem['distance'] = binding['L']['value']
                    returnArray.append(singleItem)
            except KeyError as e:
                print e
                pass
            self.subjectsCache[inputURI] = returnArray

        return returnArray
