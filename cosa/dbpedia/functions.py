import requests

def getParams():
    params = {}
    params['spotlightEndpoint'] = 'http://blah.org'
    return params


def spotlight(searchText):
    dbpParams = getParams()
    url = dbpParams['spotlightEndpoint']

    confidence = 0.1
    headers = {'Accept': 'application/json'}
    params = {'text': searchText.lower(), 'confidence': confidence}  # requests lib auto url-encodes this for us
    resp = requests.get(url=url, params=params, headers=headers)

    if 'Resources' in resp.json():
        # print resp.json()
        return resp.json()  # parse the JSON and return as a Python dict.
    else:
        #what to do here?
        return False