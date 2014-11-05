import hashlib
import urllib
import urllib2

URL = 'https://api.smartystreets.com/lists?{0}'

FILE_NAME = 'FILE_NAME_HERE'

data = open(FILE_NAME, 'rb').read()

query = {
    'filename': FILE_NAME,
    'hash': hashlib.sha1(data).hexdigest(), # optional
    'auth-id': 'AUTH-ID-HERE',
    'auth-token': 'AUTH-TOKEN-HERE'
}

request = urllib2.Request(
    URL.format(urllib.urlencode(query)),
    data=data,
    headers={ 'method': 'POST' }
)

try:
    response = urllib2.urlopen(request)
    contents = response.read()
    print response.getcode()
    print contents
except urllib2.HTTPError as error:
    print 'ERROR: {0}'.format(error.getcode())
    print error.msg
    print error.read()