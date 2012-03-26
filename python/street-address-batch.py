import json
import pprint
import urllib
import urllib2

URL = 'https://api.qualifiedaddress.com/street-address/?auth-token={0}'.format(
    urllib.quote(r'YOUR_AUTHENTICATION_TOKEN')
)

addresses = [
    {
        'street': '1 infinite loop',
        'city': 'cupertino',
        'state': 'ca',
        'zipCode': '95014',
        'candidates': '10',
    },
    {
        'street': '1600 Pennsylvania ave',
        'city': 'Washington',
        'state': 'DC',
        'zipCode': '20500',
        'candidates': '10',
    }
]

DATA = json.dumps(addresses)

request = urllib2.Request(URL, data=DATA)
response = urllib2.urlopen(request)

print pprint.pformat(json.loads(response.read()))
