import json
import pprint
import urllib

LOCATION = 'https://api.qualifiedaddress.com/street-address/'
QUERY_STRING = urllib.urlencode({ # entire query sting must be URL-Encoded
    'auth-token': r'Your Authentication Token',
    'street': '1600 Pennsylvania Ave NW',
    'city': 'Washington',
    'state': 'DC',
    'zipCode': '20500',
    'candidates': '10',
})
URL = LOCATION + '?' + QUERY_STRING

response = urllib.urlopen(URL).read()
structure = json.loads(response)
pprint.pprint(structure)

# SAMPLE OUTPUT:
#
#[{u'analysis': {u'dpv_cmra': u'N',
#                u'dpv_footnotes': u'AAN1',
#                u'dpv_match_code': u'D',
#                u'dpv_vacant': u'N',
#                u'ews_match': False,
#                u'footnotes': u'H#'},
#  u'candidate_index': 0,
#  u'components': {u'city_name': u'WASHINGTON',
#                  u'delivery_point': u'99',
#                  u'delivery_point_check_digit': u'2',
#                  u'plus4_code': u'0003',
#                  u'primary_number': u'1600',
#                  u'state_abbreviation': u'DC',
#                  u'street_name': u'PENNSYLVANIA',
#                  u'street_postdirection': u'NW',
#                  u'street_suffix': u'AVE',
#                  u'zipcode': u'20500'},
#  u'delivery_line_1': u'1600 PENNSYLVANIA AVE NW',
#  u'delivery_point_barcode': u'205000003992',
#  u'input_index': 0,
#  u'last_line': u'WASHINGTON DC 20500-0003',
#  u'metadata': {u'building_default_indicator': u'Y',
#                u'carrier_route': u'C000',
#                u'congressional_district': u'AL',
#                u'county_fips': u'11001',
#                u'county_name': u'DISTRICT OF COLUMBIA',
#                u'record_type': u'H'}}]