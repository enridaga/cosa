import requests

class DBPedia:
  def __init__(self, spotlightEndpoint, dbpediaEndpoint):
    self.spotlightEndpoint = spotlightEndpoint
    self.dbpediaEndpoint = dbpediaEndpoint

  def spotlight(self, searchText):
      url = self.spotlightEndpoint
      confidence = 0.3
      headers = {'Accept': 'application/json'}
      params = {'text': searchText.lower(), 'confidence': confidence} #requests lib auto url-encodes this for us
      resp = requests.get(url=url, params=params, headers=headers)

      if 'Resources' in resp.json():
          #print resp.json()
          return resp.json()  # parse the JSON and return as a Python dict.
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




  def subjRequest(self, inputURI):
      url = self.dbpediaEndpoint
      headers = {'Accept': 'application/json'}
      sparqlQuery = ' \
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \
PREFIX dcterm: <http://purl.org/dc/terms/> \
SELECT ?obj ?label WHERE { \
  <' + inputURI + '> dcterm:subject ?obj . \
  ?obj rdfs:label ?label . filter (lang(?label) = "en") \
} '

      params = {'query': sparqlQuery}

      resp = requests.get(url=url, params=params, headers=headers)
      return resp.json()  # parse the JSON and return as a Python dict.

  def assocDataRequest(self, inputURI):
      url = self.dbpediaEndpoint
      headers = {'Accept': 'application/json'}
      sparqlQuery = ' \
  SELECT ?obj WHERE { \
  { \
  <' + inputURI + '> dct:subject ?obj . \
  } UNION { \
  <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something . \
    ?something dct:subject ?obj . \
  } UNION { \
  <' + inputURI + '> rdf:type ?obj . \
  } UNION { \
  <' + inputURI + '> <http://dbpedia.org/ontology/wikiPageRedirects> ?something . \
    ?something rdf:type ?obj . \
  } \
}'

      params = {'query': sparqlQuery}

      resp = requests.get(url=url, params=params, headers=headers)
      return resp.json()  # parse the JSON and return as a Python dict.

  def getSubjURIs(self, inputURI):
      returnArray = []
      fullResponse = self.subjRequest(inputURI)
      try:
          bindings = fullResponse['results']['bindings']
          for binding in bindings:
              returnArray.append(binding['obj']['value'])
              #print 'Category: ', binding['obj']['value']
      except KeyError:
          pass
      return returnArray

  def getAssocURIs(self, inputURI):
      returnArray = []
      fullResponse = self.assocDataRequest(inputURI)
      try:
          bindings = fullResponse['results']['bindings']
          for binding in bindings:
              returnArray.append(binding['obj']['value'])
              #print 'Category: ', binding['obj']['value']
      except KeyError:
          pass
      return returnArray
