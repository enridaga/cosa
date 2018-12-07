import requests

class DBPedia:
  def __init__(self, spotlightEndpoint, dbpediaEndpoint):
    self.spotlightEndpoint = spotlightEndpoint
    self.dbpediaEndpoint = dbpediaEndpoint

  def spotlight(self, searchText, confidence):
      url = self.spotlightEndpoint
      #confidence = 0.3
      headers = {'Accept': 'application/json'}
      params = {'text': searchText.lower(), 'confidence': confidence} #requests lib auto url-encodes this for us
      resp = requests.get(url=url, params=params, headers=headers)

      if 'Resources' in resp.json():
          #print resp.json()
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

      resp = requests.get(url=url, params=params, headers=headers)
      return resp.json()  # parse the JSON and return as a Python dict.

  def dbpediaCategoriesTransitive(self, category):
      sparqlQuery = '\
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> \
SELECT distinct ?category WHERE { \
  <http://dbpedia.org/resource/Category:Reptiles_of_South_America> skos:broader{,10} ?category \
}'
      return self.dbpediaEndpointRequest(sparqlQuery)
      

  #Does a full request and returns the raw result
  def dbpediaRequestEntities(self, inputURI):
    sparqlQuery = ' \
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> \
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \
PREFIX dct: <http://purl.org/dc/terms/> \
SELECT distinct ?obj ?T WHERE { \
  { \
  <' + inputURI + '> dct:subject ?obj . \
    bind("S" as ?T) \
  } UNION { \
  <' + inputURI + '> dct:subject/skos:broader ?obj . \
    bind("S" as ?T) \
  } UNION { \
  <' + inputURI + '> dct:subject/skos:broader/skos:broader ?obj . \
    bind("S" as ?T) \
  } UNION { \
  <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something . \
    ?something dct:subject ?obj . \
    bind("S" as ?T) \
  } UNION { \
  <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something . \
    ?something dct:subject/skos:broader ?obj . \
    bind("S" as ?T) \
  } UNION { \
  <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something .  \
    ?something dct:subject/skos:broader/skos:broader ?obj . \
    bind("S" as ?T) \
  } UNION { \
  <' + inputURI + '> rdf:type ?obj . \
        bind("T" as ?T) \
  } UNION { \
  <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something . \
    ?something rdf:type ?obj . \
        bind("T" as ?T) \
  } \
}'
    return self.dbpediaEndpointRequest(sparqlQuery)

  #Abstraction of dbpediaEndpointRequest(), just returns simplified Subject and Type URIs
  #USE THIS FOR MOST USES
  def getSubjTypeURIs(self,inputURI):
      returnArray = []
      fullResponse = self.dbpediaRequestEntities(inputURI)
      try:
          bindings = fullResponse['results']['bindings']
          for binding in bindings:
              singleItem = {}
              singleItem['uri'] = binding['obj']['value']
              singleItem['type'] = binding['T']['value']
              returnArray.append(singleItem)
              #print 'Category: ', binding['obj']['value']
      except KeyError:
          pass
      return returnArray

  #just get the Subject URIs
  def getSubjURIs(self, inputURI):
      returnArray = []
      fullResponse = self.dbpediaRequestEntities(inputURI)
      try:
          bindings = fullResponse['results']['bindings']
          for binding in bindings:
              singleItem = {}
              singleItem['uri'] = binding['obj']['value']
              singleItem['type'] = binding['T']['value']
              if singleItem['type'] == 'S':
                returnArray.append(singleItem)
              # print 'Category: ', binding['obj']['value']
      except KeyError:
          pass
      return returnArray

  #Just get the type URIs
  def getTypeURIs(self, inputURI):
      returnArray = []
      fullResponse = self.dbpediaRequestEntities(inputURI)
      try:
          bindings = fullResponse['results']['bindings']
          for binding in bindings:
              singleItem = {}
              singleItem['uri'] = binding['obj']['value']
              singleItem['type'] = binding['T']['value']
              if singleItem['type'] == 'T':
                returnArray.append(singleItem)
              # print 'Category: ', binding['obj']['value']
      except KeyError:
          pass
      return returnArray


