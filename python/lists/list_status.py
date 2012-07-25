import json
from pprint import pprint
from urllib import urlencode
import urllib2

URL = 'https://api.smartystreets.com/lists/{0}/?{1}'

query = {
    'auth-id': 'AUTH-ID-HERE',
    'auth-token': 'AUTH-TOKEN-HERE'
}

list_id = 'LIST-ID-HERE'

request = urllib2.Request(URL.format(list_id, urlencode(query)))
request.get_method = lambda: 'GET'

try:
    response = urllib2.urlopen(request)
    contents = response.read()
    print response.getcode()
    pprint(json.loads(contents))
except urllib2.HTTPError as error:
    print 'ERROR: {0}'.format(error.getcode())
    print error.msg
    print error.read()