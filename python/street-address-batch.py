import json
import pprint
import urllib
import urllib2

# Obtain an authentication ID/token pair from your
# SmartyStreets account and put them in below.

URL = "https://api.smartystreets.com/street-address/?auth-id={0}&auth-token={1}".format(
    urllib.quote(r"<auth id here>"),
    urllib.quote(r"<raw auth token here>")
)

addresses = [
    {
        "street": "1 infinite loop",
        "city": "cupertino",
        "state": "ca",
        "zipcode": "95014",
        "candidates": 10,
    },
    {
        "street": "1600 Pennsylvania ave",
        "city": "Washington",
        "state": "DC",
        "zipcode": "20500",
        "candidates": 10,
    }
]

DATA = json.dumps(addresses)

request = urllib2.Request(URL, data=DATA)
response = urllib2.urlopen(request)

print pprint.pformat(json.loads(response.read()))
