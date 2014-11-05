import json
import pprint
import urllib

# Obtain an authentication ID/token pair from your
# SmartyStreets account and put them in below.

LOCATION = "https://api.smartystreets.com/street-address/"
QUERY_STRING = urllib.urlencode({   # entire query sting must be URL-Encoded
    "auth-id": r"<ID VALUE>",
    "auth-token": r"<RAW TOKEN VALUE>",
    "street": "1 infinite loop",
    "city": "cupertino",
    "state": "ca",
    "zipcode": "95014",
    "candidates": "1",
})
URL = LOCATION + "?" + QUERY_STRING

response = urllib.urlopen(URL).read()
structure = json.loads(response)
pprint.pprint(structure)

# SAMPLE OUTPUT:
#
#[{u'analysis': {u'dpv_cmra': u'N',
#                u'dpv_footnotes': u'AABB',
#                u'dpv_match_code': u'Y',
#                u'dpv_vacant': u'N',
#                u'ews_match': False},
#  u'candidate_index': 0,
#  u'components': {u'city_name': u'Cupertino',
#                  u'delivery_point': u'01',
#                  u'delivery_point_check_digit': u'7',
#                  u'plus4_code': u'2083',
#                  u'primary_number': u'1',
#                  u'state_abbreviation': u'CA',
#                  u'street_name': u'Infinite',
#                  u'street_suffix': u'Loop',
#                  u'zipcode': u'95014'},
#  u'delivery_line_1': u'1 Infinite Loop',
#  u'delivery_point_barcode': u'950142083017',
#  u'input_index': 0,
#  u'last_line': u'Cupertino CA 95014-2083',
#  u'metadata': {u'carrier_route': u'C067',
#                u'congressional_district': u'15',
#                u'county_fips': u'06085',
#                u'county_name': u'Santa Clara',
#                u'latitude': 37.33118,
#                u'longitude': -122.03062,
#                u'precision': u'Zip9',
#                u'record_type': u'S'}}]
