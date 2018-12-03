import requests

def getParams():
    params = {}
    params['spotlightEndpoint'] = 'http://anne.kmi.open.ac.uk/rest/annotate'
    params['dbpediaEndpoint'] = 'http://dbpedia.org/sparql'
    return params


def spotlight(searchText, confidence):
    dbpParams = getParams()
    url = dbpParams['spotlightEndpoint']

    #confidence = 0.1
    headers = {'Accept': 'application/json'}
    params = {'text': searchText.lower(), 'confidence': confidence}  # requests lib auto url-encodes this for us
    resp = requests.get(url=url, params=params, headers=headers)

    if 'Resources' in resp.json():
        # print resp.json()
        return resp.json()  # parse the JSON and return as a Python dict.
    else:
        #what to do here?
        return False