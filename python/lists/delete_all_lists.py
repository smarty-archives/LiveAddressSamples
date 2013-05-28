"""
WARNING: this script will delete all lists on the specified account! This cannot be undone...
"""

import json
import urllib
import urllib2


STATUS_URL = 'https://api.smartystreets.com/lists?{0}'
DELETE_URL = 'https://api.smartystreets.com/lists/{0}?{1}'


query = {
    'auth-id': 'YOUR_AUTH_ID',
    'auth-token': 'YOUR_AUTH_TOKEN'
}

request = urllib2.Request(STATUS_URL.format(urllib.urlencode(query)))
response = urllib2.urlopen(request)
lists = json.loads(response.read())
print 'Deleting {0} lists...'.format(len(lists))

for l in lists:
    list_id = l['list_id']
    print 'Deleting list: {0}'.format(list_id)
    delete_url = DELETE_URL.format(list_id, urllib.urlencode(query))
    request = urllib2.Request(delete_url)
    request.get_method = lambda: 'DELETE'

    try:
        response = urllib2.urlopen(request)
        contents = response.read()
        print response.getcode()
        print contents
    except urllib2.HTTPError as error:
        print 'ERROR: {0}'.format(error.getcode())
        print error.msg
        print error.read()

print 'Finished.'