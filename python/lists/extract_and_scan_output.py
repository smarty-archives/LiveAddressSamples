"""
It is becoming more and more common for developers to parse/scan the output
of the LiveAddress for Lists service using automated scripts/programs.
While SmartyStreets will not EVER rename or remove existing fields, we
occasionally introduce new fields (which may alter the order of existing
fields). Because of this it is wise to scan in a flexible way such that your
script can absorb additive changes gracefully. This script is a simple example
that illustrates the following:

    1. Extract the files in the zip archive.
    2. Process each file by building an index between expected field names and
       their index in the actual file.
    3. Enumerate each record in each file (facilitated by the header index
       created in step 2).

Because the 'index' of headers is built from scratch at startup, the field order
can change and new fields can be added at any time and this script will not be
adversely effected.

This script expects the following command line parameters:

    1. <path-to-list-archive>: the path to the downloaded list archive
    2. <file-extension>: "txt" (delimiter == '\t') or "csv" (delimiter == ',')

For example:

  `python extract_and_scan_output.py ./my-file--2013-01-01.zip txt`

You may provide your own code in each `process_xxx` method.

"""


import os
import sys
import zipfile


def main(list_path, extension):
    FILE_PROCESSORS = {
        'everything.{0}'.format(extension): process_everything,
        'components.{0}'.format(extension): process_components,
        'simple-mailable.{0}'.format(extension): process_mailable,
        'simple-rejected.{0}'.format(extension): process_rejected,
        'simple-duplicates.{0}'.format(extension): process_duplicates,
    }

    assert os.path.exists(list_path), '{0} does NOT exist (and it ' \
                                      'should)!'.format(list_path)
    assert zipfile.is_zipfile(list_path), '{0} is NOT a zip file (it ' \
                                          'should be)!'.format(list_path)

    archive = zipfile.ZipFile(list_path, 'r')
    delimiter = ALLOWED_EXTENSIONS[extension]

    for filename in archive.namelist():
        if filename not in FILE_PROCESSORS:
            # this `continue` allows for SmartyStreets to safely
            # add other files later.
            continue

        data = archive.read(filename)[BYTE_ORDER_MARK:].strip()
        lines = data.split('\n')
        # this is the header index:
        headers = {x: i for i, x in enumerate(lines[0].split(delimiter))}

        # This aggregation of records will be extremely slow/memory-hungry
        # for large files:
        records = [line.split(delimiter) for line in lines[1:]]

        # process each expected file:
        FILE_PROCESSORS[filename](headers, records)


def process_everything(header, records):
    for record in records:
        print 'This is a record from the `everything` file:'.format(
            record[header[EVERYTHING_FIELDS[0]]])


def process_mailable(header, records):
    for record in records:
        print 'This is a mailable record: {0}'.format(
            record[header[MAILABLE_FIELDS[0]]])


def process_rejected(header, records):
    for record in records:
        print 'This is a rejected record: {0}'.format(
            record[header[REJECTED_FIELDS[0]]])


def process_components(header, records):
    for record in records:
        print 'This is a componentized record: {0}'.format(
            record[header[COMPONENTS_FIELDS[0]]])


def process_duplicates(header, records):
    for record in records:
        print 'This is a duplicate record: {0}'.format(
            record[header[DUPLICATES_FIELDS[0]]])


EVERYTHING_FIELDS = [
    'Sequence',
    'Duplicate',
    'Deliverable',
    'FirmName',
    'DeliveryLine1',
    'DeliveryLine2',
    'Urbanization',
    'City',
    'State',
    'FullZIPCode',
    'ZIPCode',
    'AddonCode',
    'PMBUnit',
    'PMBNumber',
    'ProcessFlag',
    'FlagReason',
    'Footnotes',
    'EWS',
    'CountyFips',
    'CountyName',
    'DPVCode',
    'DPVFootnotes',
    'CMRA',
    'Vacant',
    'Active',
    'DefaultFlag',
    'LACSInd',
    'LACSLinkCode',
    'LACSLinkInd',
    'DeliveryPoint',
    'CheckDigit',
    'DeliveryPointBarcode',
    'CarrierRoute',
    'RecordType',
    'Latitude',
    'Longitude',
    'Precision',
    'CongressionalDistrict',
    'RDI',
    'ELotSequence',
    'ELotSort',
    'SuiteLinkMatch',
]
MAILABLE_FIELDS = [
    'Sequence',
    'FirmName',
    'DeliveryLine1',
    'DeliveryLine2',
    'City',
    'State',
    'FullZIPCode',
    'DeliveryPointBarcode',
]
REJECTED_FIELDS = [
    'Sequence',
    'FirmName',
    'DeliveryLine1',
    'DeliveryLine2',
    'City',
    'State',
    'FullZIPCode',
    'DeliveryPointBarcode',
    'ProcessFlag',
    'FlagReason',
    'Footnotes',
    'DpvCode',
    'DpvFootnotes',
    'Vacant',
    'Active',
]
DUPLICATES_FIELDS = [
    'Sequence',
    'Deliverable',
    'FirmName',
    'DeliveryLine1',
    'DeliveryLine2',
    'City',
    'State',
    'FullZIPCode',
    'DeliveryPointBarcode',
]
COMPONENTS_FIELDS = [
    'Sequence',
    'Duplicate',
    'Deliverable',
    'PrimaryNumber',
    'StreetName',
    'StreetPredirection',
    'StreetPostdirection',
    'StreetSuffix',
    'SecondaryNumber',
    'SecondaryDesignator',
    'ExtraSecondaryNumber',
    'ExtraSecondaryDesignator',
    'PmbDesignator',
    'PmbNumber',
    'CityName',
    'StateAbbreviation',
    'ZipCode',
    'Plus4Code',
    'DeliveryPoint',
    'DeliveryPointCheckDigit',
    'Urbanization',
]
ALLOWED_EXTENSIONS = {
    'csv': ',',
    'txt': '\t',
}
BYTE_ORDER_MARK = 3


if __name__ == '__main__':
    if not sys.argv or len(sys.argv) < 3:
        print 'Usage: python extract_and_scan_output.py ' \
              '<path-to-list-archive> <file-extension>'
    elif sys.argv[-1] not in ALLOWED_EXTENSIONS:
        print 'File extension must be "csv" or "txt".'
    else:
        main(sys.argv[-2], sys.argv[-1])