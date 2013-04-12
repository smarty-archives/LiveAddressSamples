"""
This script processes a tab-delimited or .csv text file with
city/state lines and produces an output file with
city/state/zipcode combinations for the given input. In many
cases, a city/state input line will produce multiple
city/state/zipcode combinations.
"""

import json
import urllib
import urllib2


DELIMITER = '\t'  # or ',' for .csv
INPUT_FILE = 'input.txt'
OUTPUT_FILE = 'output.txt'
URL = 'https://api.smartystreets.com/zipcode?{0}'
QUERY = {
    'auth-id': '<YOUR_AUTH_ID_HERE>',
    'auth-token': '<YOUR_RAW_AUTH_TOKEN_HERE>'
}


def lookup_zip_codes():
    with open(INPUT_FILE) as raw, open(OUTPUT_FILE, 'w') as output:
        for number, line in enumerate(raw, start=1):
            if not line or DELIMITER not in line:
                print 'Bad input on line {0}, skipping line...'
                continue

            city, state = [x.strip() for x in line.split(DELIMITER)]
            response = http_get(city, state)
            if response and 'zipcodes' in response[0]:
                for option in response[0]['zipcodes']:
                    parsed = '{1}{0}{2}{0}{3}\n'.format(
                        DELIMITER, city, state, option['zipcode'])
                    print '\t' + parsed
                    output.write(parsed)
            else:
                output.write('{1}{0}{2}{0}\n'.format(DELIMITER, city, state))


def http_get(city=None, state=None, zip_code=None):
    return try_request(URL, format_query(city, state, zip_code))


def format_query(city=None, state=None, zip_code=None):
    q = dict()
    q.update(QUERY)
    if city: q['city'] = city
    if state: q['state'] = state
    if zip_code: q['zipcode'] = zip_code
    return urllib.urlencode(q)


def try_request(url, query, payload=None):
    headers = dict()
    if payload:
        headers['Content-Type'] = 'application/json'
    request = urllib2.Request(url.format(query), data=payload, headers=headers)
    try:
        response = urllib2.urlopen(request)
        contents = response.read()
        print query
        return json.loads(contents)
    except urllib2.HTTPError as error:
        print 'ERROR: {0}'.format(error.getcode())
        print error.msg
        print error.read()


if __name__ == '__main__':
    lookup_zip_codes()