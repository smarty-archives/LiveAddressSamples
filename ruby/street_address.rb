require 'cgi'
require 'json'
require 'net/http'

# Remember to URL encode anything that could have 
# spaces (street, city) or special characters (auth-token)

URL = 'api.qualifiedaddress.com'
STREET = CGI::escape('1600 Pennsylvania Ave')
CITY = CGI::escape('Washington')
STATE = 'DC'
ZIP_CODE = '20500'
NUMBER_OF_CANDIDATES = '3'
AUTH_TOKEN = CGI::escape('YOUR KEY HERE')

QUERY_STRING = '/street-address/?' +
 	'street=' + STREET +
	'&city=' + CITY +
	'&state=' + STATE +
	'&zipcode=' + ZIP_CODE +
	'&candidates=' + NUMBER_OF_CANDIDATES +
	'&auth-token=' + AUTH_TOKEN

http = Net::HTTP.new(URL)
request = Net::HTTP::Get.new(QUERY_STRING)
response = http.request(request)
puts JSON.pretty_generate(JSON.parse(response.body))

# SAMPLE OUTPUT:
#
# [
#   {
#     "input_index": 0,
#     "candidate_index": 0,
#     "delivery_line_1": "1600 PENNSYLVANIA AVE NW",
#     "last_line": "WASHINGTON DC 20500-0003",
#     "delivery_point_barcode": "205000003992",
#     "components": {
#       "primary_number": "1600",
#       "street_name": "PENNSYLVANIA",
#       "street_postdirection": "NW",
#       "street_suffix": "AVE",
#       "city_name": "WASHINGTON",
#       "state_abbreviation": "DC",
#       "zipcode": "20500",
#       "plus4_code": "0003",
#       "delivery_point": "99",
#       "delivery_point_check_digit": "2"
#     },
#     "metadata": {
#       "record_type": "H",
#       "county_fips": "11001",
#       "county_name": "DISTRICT OF COLUMBIA",
#       "carrier_route": "C000",
#       "congressional_district": "AL",
#       "building_default_indicator": "Y"
#     },
#     "analysis": {
#       "dpv_match_code": "D",
#       "dpv_footnotes": "AAN1",
#       "dpv_cmra": "N",
#       "dpv_vacant": "N",
#       "ews_match": false,
#       "footnotes": "H#L#"
#     }
#   }
# ]
