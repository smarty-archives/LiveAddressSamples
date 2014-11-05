from urllib import urlencode
import urllib2

URL = 'https://api.smartystreets.com/lists/{0}/download/?{1}'

query = {
    'auth-id': 'AUTH-ID-HERE',
    'auth-token': 'AUTH-TOKEN-HERE'
}

list_id = 'LIST-ID-HERE'

request = urllib2.Request(URL.format(list_id, urlencode(query)))
request.get_method = lambda: 'GET'

response = urllib2.urlopen(request)
print response.getcode()
with open('list-full.zip', 'wb') as output:
    output.write(response.read())

