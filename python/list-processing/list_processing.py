"""
--------------------------------------------------------------------------------

Requirements:

- Internet connection
- Python 2.7 (https://www.python.org/downloads/)
- Active LiveAddress API subscription (http://smartystreets.com/pricing)
- Valid Secret Key Pair (http://smartystreets.com/account/keys)

--------------------------------------------------------------------------------

This program preserves the core functionality of the deprecated LiveAddress
for Lists service by translating the output of the LiveAddress API into a
text file but without concerning itself with much of the backend infrastructure 
associated with the deprecated service (asynchronous messaging infrastructure, 
a fleet of auto-scaled processing servers, queueing of lists, web GUI, free 
file storage). Our reason for writing this code was to illustrate that our 
LiveAddress for Lists service was, in essence, a well-crafted example of how 
to use the LiveAddress API to do something interesting. In the case of 
LiveAddress for Lists, the "interesting" thing was to process a file with 
address data.

The input file must be a TAB-DELIMITED text file with a header row that has
column names from the following set (case-insensitive):

    'Id'
    'FullName'
    'FirstName'
    'LastName'
    'OrganizationName'
    'Street1'
    'Secondary'
    'Street2'
    'City'
    'State'
    'ZipCode'
    'CityStateZipCode'
    'Plus4Code'
    'Urbanization'

The column names may be presented in any order, but each record's field data
must match that order. Additional fields are welcome as well, but they won't be
included in the requests to the LiveAddress API.

The only combination of fields that is required is one of the following:

Street1, ZipCode
Street1, City, State
Street1, City, State, ZipCode
Street1, LastLine (city/state/zipcode in a single field)

The output of this program is a file that contains every field from the JSON
response of the LiveAddress API.

    Usage: python list_processing.py <path-to-input-file> <path-to-output-file>

--------------------------------------------------------------------------------

It should be noted that this program contains logic that we've used at
SmartyStreets for some time now. Much of the logic (like de-duplication and
deciding which fields to use for the 'addressee') are general purpose. You might
have good reasons to rewrite portions of this program in a way that matches your
use case more specifically.

--------------------------------------------------------------------------------

LiveAddress API Documentation:

- http://smartystreets.com/kb/liveaddress-api/rest-endpoint
- http://smartystreets.com/kb/liveaddress-api/parsing-the-response
- http://smartystreets.com/kb/liveaddress-api/field-definitions

--------------------------------------------------------------------------------

Enjoy!
"""


import argparse
import hashlib
import httplib
import io
import json
import os
import traceback
import urllib
import urllib2

# NOTE: config.py is where the authentication credentials are currently stored:
import config


def main(input_file, output_file):
    header_line, headers = analyze(input_file)
    if headers is None:
        exit(1)

    with io.open(input_file) as records, io.open(output_file, 'w') as output:
        write_header_row(header_line, output)
        process(records, headers, output)
        output.flush()


################################################################################
# Analysis of file header and contents                                         #
################################################################################


def analyze(input_file):
    """
    Does the input file exist?
    Does it have a header row with the right kind of field names?
    Does each record have the appropriate number of fields?
    """

    if not os.path.exists(input_file):
        print 'The given input file does not exist!'
        return None, None

    header_line = None
    headers = None
    with io.open(input_file) as records:
        columns = 0
        header = ''

        for number, line in enumerate(records, start=1):
            if number == 1:
                header = line
                fields = line.split(TAB)
                columns = len(fields)
                headers = identify_headers(fields)
                if headers is None:
                    return None, None
                else:
                    header_line = line

            field_count = line.count(TAB) + 1
            if field_count != columns:
                print 'Line number {0} had {1} fields but each record ' \
                      'must have {2} fields (separated by tabs) to ' \
                      'match the header row: "{3}"' \
                    .format(number, field_count, columns, header)
                return None, None

    return header_line, headers


def identify_headers(fields):
    """
    Required: Street1 & (ZIP_CODE | CITY & STATE | LAST_LINE)
    """

    headers = dict.fromkeys(Headers.field_keys())
    for index, field in enumerate(fields):
        field = field.strip().lower()
        headers[field] = index

    for header in headers.keys():
        if headers[header] is None:
            del headers[header]

    if headers.get(Headers.STREET1) is None:
        print 'You must include a "Street1" field in the header row!'
        return None

    if headers.get(Headers.ZIP_CODE) is not None:
        return headers

    if headers.get(Headers.LAST_LINE) is not None:
        return headers

    if (headers.get(Headers.CITY) is not None and
            headers.get(Headers.STATE) is not None):
        return headers

    print 'At minimum, you must include "Street1" and at least one ' \
          'of the following combinations:\n\t' \
          '"ZipCode"\n\t' \
          '"CityStateZipCode"\n\t' \
          '"City", "State"'
    return None


def write_header_row(header_line, output):
    """
    Inserts the headers from the input file into the output file header row.
    """

    header_fields = header_line.strip().split(TAB)
    header_fields = TAB.join(['[{0}]'.format(x) for x in header_fields])
    output_header_row = Templates.header.format(
        input_headers=header_fields)
    output.write(output_header_row)


################################################################################
# Processing of address records                                                #
################################################################################


def process(records, headers, output):
    """
    Each HTTP request payload is a batch of <= 100 addresses (json).
    HTTP error (other than 400) causes unhandled exception (program exits).
    """

    batch = []
    hashes = set()

    for number, line in enumerate(records):
        if not number:
            continue

        input_record = InputRecord(line, headers)
        if len(batch) >= 100:
            verified_batch, ok = verify(batch)
            if not ok:
                return

            write_batch(verified_batch, hashes, output)
            batch[:] = []

        batch.append(input_record)

    if len(batch):
        verified_batch, ok = verify(batch)
        if not ok:
            return

        write_batch(verified_batch, hashes, output)


def is_duplicate(hashes, record):
    """
    Each address result is concatenated and hashed using MD5. `hashes` set
    maintains record of everything we've already seen.
    """

    value = record.hash_input()
    if value == BLANK_ADDRESS_CONCATENATION:
        return False

    hasher = hashlib.md5()
    hasher.update(value)
    hashed = hasher.digest()

    if hashed in hashes:
        return True

    hashes.add(hashed)
    return False


def verify(batch):
    """
    LiveAddress API - HTTP nitty-gritty.
    """

    records = sanitize(batch)
    payload = json.dumps(records)
    url = HTTP.api_url + '?' + urllib.urlencode(config.AUTHENTICATION)
    request = urllib2.Request(url, payload, HTTP.request_headers)
    first = batch[0].sequence
    last = batch[-1].sequence

    # Disables PyCharm warning:
    # noinspection PyBroadException
    try:
        response = urllib2.urlopen(request)
        return parse(response.read(), batch), True
    except urllib2.HTTPError, e:
        if e.code == 400:
            print 'Bad batch from records {0}-{1}, returning ' \
                  'empty result set... ({2})'.format(first, last, e.reason)
            print payload
            return [], True
        else:
            print 'urllib2.HTTPError: HTTP Status Code for batch of records ' \
                  '({0}-{1}): {2} ({3})'.format(first, last, e.code, e.reason)
            print payload
            return [], False
    except urllib2.URLError, e:
        print 'urllib2.URLError for batch of records ' \
              '({0}-{1}):\n\tMessage: {2}\n\tReason: {3}' \
            .format(first, last, e.message, e.reason)
        print payload
        return [], False
    except httplib.HTTPException, e:
        print 'httplib.HTTPException for batch of records ' \
              '({0}-{1}): {2}'.format(first, last, e.message)
        print payload
        return [], False
    except Exception:
        print 'Exception for batch of records ({0}-{1}): {2}' \
            .format(first, last, traceback.format_exc())
        print payload
        return [], False


def sanitize(input_batch):
    """
    Make sure the JSON payload will have the correct fields (and not
    any extra fields).
    """

    records = [x.to_dict() for x in input_batch]
    for record in records:
        if not record.get('street'):
            record['street'] = '<unknown_street>'
            # response: '<Unknown_Street>'

        if (not record.get('zipcode')
                and not record.get('state')
                and not record.get('city')
                and not record.get('lastline')):
            record['lastline'] = '<lastline_unknown>'
            # response: 'Lastline Unknown'

    for record in records:
        for field in record.keys():
            if not record[field].strip():
                del record[field]

    return records


def parse(json_result, input_batch):
    """
    Put the resulting JSON response into a well-formed structure.
    """

    results = json.loads(json_result)
    batch = []
    for item in input_batch:
        processed = AddressResponse()
        processed.include_input(item)
        batch.append(processed)

    for index, result in enumerate(results):
        batch_index = int(result['input_index'])
        batch[batch_index].include_output(result)

    return batch


def write_batch(batch, hashes, output):
    for record in batch:
        if is_duplicate(hashes, record):
            record.duplicate = 'Y'

        output.write(unicode(record))


################################################################################
# Helpers and constants                                                        #
################################################################################


QUOTE = '"'
TAB = u'\t'
BLANK_ADDRESS_CONCATENATION = '/////'


class InputRecord(object):
    """
    The InputRecord defines the fields that will be submitted in JSON format
    to the LiveAddress API.
    """

    sequence_counter = 1

    def __unicode__(self):
        return TAB.join(x.strip().replace(QUOTE, '')
                        for x in self.original.split(TAB))

    def to_dict(self):
        return {
            # These key names must match the expected
            # LiveAddress API JSON input fields:
            'input_id': self.input_id,
            'street': self.street,
            'street2': self.street2,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'plus4': self.plus4,
            'urbanization': self.urbanization,
            'secondary': self.secondary,
            'lastline': self.lastline,
            'addressee': self.addressee,
        }

    def __init__(self, line, headers):
        self.original = line
        self.sequence = InputRecord.sequence_counter
        self.fields = [x.strip() for x in line.split(TAB)]

        self.input_id = get(self.fields, headers.get(Headers.ID))
        self.street = get(self.fields, headers.get(Headers.STREET1))
        self.street2 = get(self.fields, headers.get(Headers.STREET2))
        self.city = get(self.fields, headers.get(Headers.CITY))
        self.state = get(self.fields, headers.get(Headers.STATE))
        self.zipcode = get(self.fields, headers.get(Headers.ZIP_CODE))
        self.plus4 = get(self.fields, headers.get(Headers.PLUS4CODE))
        self.urbanization = get(self.fields, headers.get(Headers.URBANIZATION))
        self.secondary = get(self.fields, headers.get(Headers.SECONDARY))
        self.lastline = get(self.fields, headers.get(Headers.LAST_LINE))
        self.addressee = self.decide_on_addressee(headers)

        InputRecord.sequence_counter += 1
        report_progress(InputRecord.sequence_counter)

    def decide_on_addressee(self, headers):
        """
        This is the logic we've used at SmartyStreets for some time. But it
        doesn't have to be like this if it's not helpful.
        """
        organization = get(self.fields, headers.get(Headers.ORGANIZATION))
        if organization:
            return organization

        full = get(self.fields, headers.get(Headers.FULL_NAME))
        if full:
            return full

        first = get(self.fields, headers.get(Headers.FIRST_NAME))
        last = get(self.fields, headers.get(Headers.LAST_NAME))
        return (first + ' ' + last).strip()


def get(items, index):
    """
    Safe indexing of list (avoids IndexError and subsequent try-except block).
    Also strips leading and trailing whitespace and leading and trailing quotes.
    """

    if index is None:
        return ''

    if index >= len(items) or index < 0:
        print 'Tried to access an invalid index in the line! ' \
              'Index: {0} | FieldCount: {1}'.format(index, len(items))
        return ''

    return items[index].strip().replace(QUOTE, '')


def report_progress(sequence):
    if not sequence % 1000:
        print sequence


class AddressResponse(object):
    """
    The AddressResponse serves to convert the JSON response from the
    LiveAddress API to the tab-delimited format of the output file.
    Each instance of this class corresponds directly to a record in
    the output file.
    """

    def hash_input(self):
        """
        The value returned is hashed and used to determine duplicate
        addresses across the entire list/file. These are the values we've
        used for some time to de-duplicate. Feel free to modify this method
        if you have a more appropriate implementation for your use case.
        """

        return '{0}/{1}/{2}/{3}/{4}/{5}'.format(
            self.delivery_line_1,
            self.delivery_line_2,
            self.city_name,
            self.state_abbreviation,
            self.zipcode + self.plus4_code,
            self.urbanization)

    def include_input(self, input_record):
        """
        Keeps track of all input fields as they are included in the output file.
        """

        self.sequence = input_record.sequence
        self.input = input_record

    def include_output(self, structure):
        """
        Logic to convert JSON structure to a tab-delimited record.
        """

        analysis = structure.get('analysis') or {}
        component = structure.get('components') or {}
        metadata = structure.get('metadata') or {}

        self.input_id = structure.get('input_id') or ''
        self.input_index = structure.get('input_index') or ''
        self.candidate_index = structure.get('candidate_index') or ''
        self.addressee = structure.get('addressee') or ''
        self.delivery_line_1 = structure.get('delivery_line_1') or ''
        self.delivery_line_2 = structure.get('delivery_line_2') or ''
        self.last_line = structure.get('last_line') or ''
        self.delivery_point_barcode = structure.get('delivery_point_barcode') or ''
        self.urbanization = component.get('urbanization') or ''
        self.primary_number = component.get('primary_number') or ''
        self.street_name = component.get('street_name') or ''
        self.street_predirection = component.get('street_predirection') or ''
        self.street_postdirection = component.get('street_postdirection') or ''
        self.street_suffix = component.get('street_suffix') or ''
        self.secondary_number = component.get('secondary_number') or ''
        self.secondary_designator = component.get('secondary_designator') or ''
        self.extra_secondary_number = component.get('extra_secondary_number') or ''
        self.extra_secondary_designator = component.get('extra_secondary_designator') or ''
        self.pmb_designator = component.get('pmb_designator') or ''
        self.pmb_number = component.get('pmb_number') or ''
        self.city_name = component.get('city_name') or ''
        self.default_city_name = component.get('default_city_name') or ''
        self.state_abbreviation = component.get('state_abbreviation') or ''
        self.zipcode = component.get('zipcode') or ''
        self.plus4_code = component.get('plus4_code') or ''
        self.delivery_point = component.get('delivery_point') or ''
        self.delivery_point_check_digit = component.get('delivery_point_check_digit') or ''
        self.record_type = metadata.get('record_type') or ''
        self.zip_type = metadata.get('zip_type') or ''
        self.county_fips = metadata.get('county_fips') or ''
        self.county_name = metadata.get('county_name') or ''
        self.carrier_route = metadata.get('carrier_route') or ''
        self.congressional_district = metadata.get('congressional_district') or ''
        self.building_default_indicator = metadata.get('building_default_indicator') or ''
        self.rdi = metadata.get('rdi') or ''
        self.elot_sequence = metadata.get('elot_sequence') or ''
        self.elot_sort = metadata.get('elot_sort') or ''
        self.latitude = metadata.get('latitude') or ''
        self.longitude = metadata.get('longitude') or ''
        self.precision = metadata.get('precision') or ''
        self.time_zone = metadata.get('time_zone') or ''
        self.utc_offset = metadata.get('utc_offset') or ''
        self.dst = metadata.get('dst') or ''
        self.dpv_match_code = analysis.get('dpv_match_code') or ''
        self.dpv_footnotes = analysis.get('dpv_footnotes') or ''
        self.dpv_cmra = analysis.get('dpv_cmra') or ''
        self.dpv_vacant = analysis.get('dpv_vacant') or ''
        self.active = analysis.get('active') or ''
        self.ews_match = analysis.get('ews_match') or ''
        self.footnotes = analysis.get('footnotes') or ''
        self.lacslink_code = analysis.get('lacslink_code') or ''
        self.lacslink_indicator = analysis.get('lacslink_indicator') or ''
        self.suitelink_match = analysis.get('suitelink_match') or ''

    def _to_dict(self):
        return {
            # These key names must match those in the Template.row!
            'sequence': self.sequence,
            'duplicate': self.duplicate,
            'input_id': self.input_id,
            'input_index': self.input_index,
            'candidate_index': self.candidate_index,
            'addressee': self.addressee,
            'delivery_line_1': self.delivery_line_1,
            'delivery_line_2': self.delivery_line_2,
            'last_line': self.last_line,
            'delivery_point_barcode': self.delivery_point_barcode,
            'urbanization': self.urbanization,
            'primary_number': self.primary_number,
            'street_name': self.street_name,
            'street_predirection': self.street_predirection,
            'street_postdirection': self.street_postdirection,
            'street_suffix': self.street_suffix,
            'secondary_number': self.secondary_number,
            'secondary_designator': self.secondary_designator,
            'extra_secondary_number': self.extra_secondary_number,
            'extra_secondary_designator': self.extra_secondary_designator,
            'pmb_designator': self.pmb_designator,
            'pmb_number': self.pmb_number,
            'city_name': self.city_name,
            'default_city_name': self.default_city_name,
            'state_abbreviation': self.state_abbreviation,
            'zipcode': self.zipcode,
            'plus4_code': self.plus4_code,
            'delivery_point': self.delivery_point,
            'delivery_point_check_digit': self.delivery_point_check_digit,
            'record_type': self.record_type,
            'zip_type': self.zip_type,
            'county_fips': self.county_fips,
            'county_name': self.county_name,
            'carrier_route': self.carrier_route,
            'congressional_district': self.congressional_district,
            'building_default_indicator': self.building_default_indicator,
            'rdi': self.rdi,
            'elot_sequence': self.elot_sequence,
            'elot_sort': self.elot_sort,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'precision': self.precision,
            'time_zone': self.time_zone,
            'utc_offset': self.utc_offset,
            'dst': self.dst,
            'dpv_match_code': self.dpv_match_code,
            'dpv_footnotes': self.dpv_footnotes,
            'dpv_cmra': self.dpv_cmra,
            'dpv_vacant': self.dpv_vacant,
            'active': self.active,
            'ews_match': self.ews_match,
            'footnotes': self.footnotes,
            'lacslink_code': self.lacslink_code,
            'lacslink_indicator': self.lacslink_indicator,
            'suitelink_match': self.suitelink_match,
        }

    def __unicode__(self):
        """
        Turns self into a tab-delimited unicode string for the output file.''
        """

        output = Templates.row.format(**self._to_dict())
        with_input = output.format(all_input_fields=unicode(self.input))
        return with_input

    def __init__(self):
        self.input = None
        self.sequence = -1
        self.duplicate = ''
        self.input_id = ''
        self.input_index = ''
        self.candidate_index = ''
        self.addressee = ''
        self.delivery_line_1 = ''
        self.delivery_line_2 = ''
        self.last_line = ''
        self.delivery_point_barcode = ''
        self.urbanization = ''
        self.primary_number = ''
        self.street_name = ''
        self.street_predirection = ''
        self.street_postdirection = ''
        self.street_suffix = ''
        self.secondary_number = ''
        self.secondary_designator = ''
        self.extra_secondary_number = ''
        self.extra_secondary_designator = ''
        self.pmb_designator = ''
        self.pmb_number = ''
        self.city_name = ''
        self.default_city_name = ''
        self.state_abbreviation = ''
        self.zipcode = ''
        self.plus4_code = ''
        self.delivery_point = ''
        self.delivery_point_check_digit = ''
        self.record_type = ''
        self.zip_type = ''
        self.county_fips = ''
        self.county_name = ''
        self.carrier_route = ''
        self.congressional_district = ''
        self.building_default_indicator = ''
        self.rdi = ''
        self.elot_sequence = ''
        self.elot_sort = ''
        self.latitude = ''
        self.longitude = ''
        self.precision = ''
        self.time_zone = ''
        self.utc_offset = ''
        self.dst = ''
        self.dpv_match_code = ''
        self.dpv_footnotes = ''
        self.dpv_cmra = ''
        self.dpv_vacant = ''
        self.active = ''
        self.ews_match = ''
        self.footnotes = ''
        self.lacslink_code = ''
        self.lacslink_indicator = ''
        self.suitelink_match = ''


class Headers(object):
    ID = 'Id'.lower()
    FULL_NAME = 'FullName'.lower()
    FIRST_NAME = 'FirstName'.lower()
    LAST_NAME = 'LastName'.lower()
    ORGANIZATION = 'OrganizationName'.lower()
    STREET1 = 'Street1'.lower()
    STREET2 = 'Street2'.lower()
    SECONDARY = 'Secondary'.lower()
    CITY = 'City'.lower()
    STATE = 'State'.lower()
    ZIP_CODE = 'ZipCode'.lower()
    LAST_LINE = 'CityStateZipCode'.lower()
    PLUS4CODE = 'Plus4Code'.lower()
    URBANIZATION = 'Urbanization'.lower()

    @classmethod
    def field_keys(cls):
        return [
            cls.ID,

            cls.FULL_NAME, cls.FIRST_NAME, cls.LAST_NAME, cls.ORGANIZATION,

            cls.STREET1, cls.STREET2, cls.SECONDARY,

            cls.CITY, cls.STATE, cls.ZIP_CODE,
            cls.LAST_LINE, cls.PLUS4CODE,

            cls.URBANIZATION,
        ]


class HTTP(object):
    api_url = 'https://api.smartystreets.com/street-address'
    request_headers = {
        'Content-Type': 'application/json',

        'x-include-invalid': 'true',  # this non-standard header ensures that
        # we get data back for addresses that fail USPS DPV (delivery
        # point validation)
    }


class Templates(object):
    header = TAB.join([
        'sequence',
        'duplicate',
        'input_id',
        'input_index',
        'addressee',
        'delivery_line_1',
        'delivery_line_2',
        'last_line',
        'delivery_point_barcode',
        'component-urbanization',
        'component-primary_number',
        'component-street_name',
        'component-street_predirection',
        'component-street_postdirection',
        'component-street_suffix',
        'component-secondary_number',
        'component-secondary_designator',
        'component-extra_secondary_number',
        'component-extra_secondary_designator',
        'component-pmb_designator',
        'component-pmb_number',
        'component-city_name',
        'component-default_city_name',
        'component-state_abbreviation',
        'component-zipcode',
        'component-plus4_code',
        'component-delivery_point',
        'component-delivery_point_check_digit',
        'metadata-record_type',
        'metadata-zip_type',
        'metadata-county_fips',
        'metadata-county_name',
        'metadata-carrier_route',
        'metadata-congressional_district',
        'metadata-building_default_indicator',
        'metadata-rdi',
        'metadata-elot_sequence',
        'metadata-elot_sort',
        'metadata-latitude',
        'metadata-longitude',
        'metadata-precision',
        'metadata-time_zone',
        'metadata-utc_offset',
        'metadata-dst',
        'analysis-dpv_match_code',
        'analysis-dpv_footnotes',
        'analysis-dpv_cmra',
        'analysis-dpv_vacant',
        'analysis-active',
        'analysis-ews_match',
        'analysis-footnotes',
        'analysis-lacslink_code',
        'analysis-lacslink_indicator',
        'analysis-suitelink_match',
    ]) + '\n'

    row = TAB.join([
        '{sequence}',
        '{duplicate}',
        '{input_id}',
        '{input_index}',
        '{addressee}',
        '{delivery_line_1}',
        '{delivery_line_2}',
        '{last_line}',
        '{delivery_point_barcode}',
        '{urbanization}',
        '{primary_number}',
        '{street_name}',
        '{street_predirection}',
        '{street_postdirection}',
        '{street_suffix}',
        '{secondary_number}',
        '{secondary_designator}',
        '{extra_secondary_number}',
        '{extra_secondary_designator}',
        '{pmb_designator}',
        '{pmb_number}',
        '{city_name}',
        '{default_city_name}',
        '{state_abbreviation}',
        '{zipcode}',
        '{plus4_code}',
        '{delivery_point}',
        '{delivery_point_check_digit}',
        '{record_type}',
        '{zip_type}',
        '{county_fips}',
        '{county_name}',
        '{carrier_route}',
        '{congressional_district}',
        '{building_default_indicator}',
        '{rdi}',
        '{elot_sequence}',
        '{elot_sort}',
        '{latitude}',
        '{longitude}',
        '{precision}',
        '{time_zone}',
        '{utc_offset}',
        '{dst}',
        '{dpv_match_code}',
        '{dpv_footnotes}',
        '{dpv_cmra}',
        '{dpv_vacant}',
        '{active}',
        '{ews_match}',
        '{footnotes}',
        '{lacslink_code}',
        '{lacslink_indicator}',
        '{suitelink_match}',
    ]) + '\n'


################################################################################
# Startup and argument parsing                                                 #
################################################################################


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    main(args.input, args.output)
