from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import configparser
from pprint import pprint
import unicodecsv as csv
# pip install --upgrade google-api-python-client oauth2client

def py2_unicode_to_str(u):
    # unicode is only exist in python2
    assert isinstance(u, unicode)
    return u.encode('utf-8')
    
def dataset(outputFile):
    config = configparser.ConfigParser()
    config.read('config.ini')
    spreadsheet_idd = config['cosa']['data.google.spreadsheetId']
    spreadsheet_range = 'EXAMPLES!A2:G'
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scopes)
        creds = tools.run_flow(flow, store)

    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    spreadsheets = service.spreadsheets()
    sheet_metadata = spreadsheets.get(spreadsheetId=spreadsheet_idd).execute()
    sheets = sheet_metadata.get('sheets', '')
    data = []
    for t in sheets:
        s = t
        st = s.get("properties", {}).get("title", "")
        srange = st + '!A2:G'
        result = spreadsheets.values().get(spreadsheetId=spreadsheet_idd,
                                range=srange).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            # print('Who, ')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                if len(row) > 5:
                    data.append([row[6],row[4], row[5]])

    data = [list(x) for x in set(tuple(x) for x in data)]
    print("Data size: %d" % len(data))
    with open(outputFile, 'wb') as csvfile:
        writer = csv.writer(csvfile, encoding='utf-8')
        for row in data:
            writer.writerow(row)
        