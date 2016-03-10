import json
import urllib
import urllib2


AUTH_ID = 'YOUR_AUTH_ID_HERE'
AUTH_TOKEN = 'YOUR_RAW_AUTH_TOKEN_HERE'


def main():
    http_get(zip_code='20500')             # shows City/State options for that ZIP Code
    http_get('Cupertino', 'CA')            # shows ZIP Code options for that City/State combination
    http_get('Cupertino', 'CA', '95014')   # confirms that the City/State and ZIP Code match.
    http_get()                             # blank query string - HTTP 400 - bad input
    http_get(zip_code='eibn3ei2nb')        # Invalid ZIP Code
    http_get('Does not exist', 'CA')       # Invalid City
    http_get('Cupertino', 'ca', '90210')   # Conflicting City/State and ZIP Code

    http_post(str())                       # empty payload - HTTP 400 - bad input
    http_post(JSON_PAYLOAD)                # all previous examples in a single POST request


def http_get(city=None, state=None, zip_code=None):
    try_request(URL, format_query(city, state, zip_code))


def http_post(payload):
    try_request(URL, format_query(), payload=payload)


def format_query(city=None, state=None, zip_code=None):
    q = dict()
    q.update(QUERY)
    if city: q['city'] = city
    if state: q['state'] = state
    if zip_code: q['zipcode'] = zip_code
    return urllib.urlencode(q)


def try_request(url, query, payload=None):
    headers = dict()
    if payload:
        headers['Content-Type'] = 'application/json'
    request = urllib2.Request(url.format(query), data=payload, headers=headers)
    try:
        response = urllib2.urlopen(request)
        contents = response.read()
        print response.getcode()
        print json.dumps(json.loads(contents), indent=4)
    except urllib2.HTTPError as error:
        print 'ERROR: {0}'.format(error.getcode())
        print error.msg
        print error.read()


URL = 'https://us-zipcode.api.smartystreets.com/lookup?{0}'
QUERY = {
    'auth-id': AUTH_ID,
    'auth-token': AUTH_TOKEN
}
JSON_PAYLOAD = """[
    {
        "zipcode": "20500"
    },
    {
        "city": "Cupertino",
        "state": "CA"
    },
    {
        "city": "Cupertino",
        "state": "CA",
        "zipcode": "95014"
    },
    {
    },
    {
        "zipcode": "eibn3ei2nb"
    },
    {
        "city": "Does not exist",
        "state": "CA"
    },
    {
        "city": "Cupertino",
        "state": "ca",
        "zipcode": "90210"
    }
]
"""


if __name__ == '__main__':
    main()
