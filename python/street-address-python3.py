import json
import urllib
from urllib import parse, request

# Obtain an authentication ID/token pair from your
# SmartyStreets account and put them in below.

LOCATION = "https://api.smartystreets.com/street-address"
QUERY_STRING = urllib.parse.urlencode({         # entire query sting must be URL-encoded
  "auth-id": r"YOUR-AUTH-ID",
  "auth-token": r"YOUR-AUTH-TOKEN",
  "street": "1 infinite loop",
  "city": "cupertino",
  "state": "ca",
  "zipcode": "95014",
  "candidates": "1"
})
URL = LOCATION + "?" + QUERY_STRING

# Perform request, read result, and load from string into Python object
response = urllib.request.urlopen(URL).read()
results = json.loads(response.decode("utf-8"))

# Pretty print for demo purposes
pretty = json.dumps(results, sort_keys=True, indent=4)
print(pretty)

# Then, to use the results in Python, very easy... for example:
print(results[0]["delivery_line_1"])
