"""
Usage: python full_example.py <input_file_path> <output_file_path>
"""

AUTH_ID = 'YOUR_AUTH_ID_HERE'
AUTH_TOKEN = 'YOUR_AUTH_TOKEN_HERE' # this value will be url-encoded later...

URL = 'https://api.smartystreets.com/lists?{0}'
STATUS_URL = 'https://api.smartystreets.com/lists/{0}/?{1}'
DOWNLOAD_URL = 'https://api.smartystreets.com/lists/{0}/download/?{1}'


import hashlib
import json
import os
import time
import sys
import urllib
import urllib2


def main():
    args = sys.argv
    input_file = args[-2]
    input_filename = os.path.basename(input_file)
    output_file = args[-1]
    mode = 'rb' if input_file.endswith('.zip') else 'r'
    data = open(input_file, mode).read()
    list_id = submit(data, input_filename)
    if list_id is None:
        return

    time.sleep(5)
    while not finished(list_id):
        time.sleep(30)

    download(list_id, output_file)


def submit(data, filename):
    print 'Uploading list to SmartyStreets List API...'

    query = {
        'filename': filename,
        'hash': hashlib.sha1(data).hexdigest(),
        'auth-id': AUTH_ID,
        'auth-token': AUTH_TOKEN
    }

    headers = {'method': 'POST'}
    if filename.endswith('.zip'):
        headers['Content-Type'] = 'application/zip'

    request = urllib2.Request(
        URL.format(urllib.urlencode(query)),
        data=data,
        headers=headers
    )

    contents = submit_http_request(request)
    structure = json.loads(contents)
    print 'New list id:', structure['list_id']
    return structure['list_id']


def finished(list_id):
    print 'Checking status of list...',

    query = {
        'auth-id': AUTH_ID,
        'auth-token': AUTH_TOKEN
    }
    request = urllib2.Request(STATUS_URL.format(list_id, urllib.urlencode(query)))
    request.get_method = lambda: 'GET'
    contents = submit_http_request(request)
    structure = json.loads(contents)
    if structure['current_step'] == 'Processing':
        print structure['current_step'], '{0}%'.format(float(structure['step_progress']) * 100)
    else:
        print structure['current_step']
    return structure['current_step'] == 'Succeeded'


def download(list_id, output_path):
    print 'Downloading list...'
    query = {
        'auth-id': AUTH_ID,
        'auth-token': AUTH_TOKEN
    }
    request = urllib2.Request(DOWNLOAD_URL.format(list_id, urllib.urlencode(query)))
    request.get_method = lambda: 'GET'
    content = submit_http_request(request)
    with open(output_path, 'wb') as output:
        output.write(content)

    print 'List downloaded ({0}).'.format(output_path)


def submit_http_request(request, depth=0):
    if depth > 5:
        print 'List API is unavailable at this time.'
        exit()

    try:
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.HTTPError as error:
        error_code = error.getcode()
        if int(error_code) == 503:
            print 'Service unavailable (but probably starting up)...attempting submit again...'
            time.sleep(5)
            # allows one retry (recursive)
            return submit_http_request(request, depth=depth + 4)
        if int(error_code) == 404:
            time.sleep(3)
            # allows up to 5 retries
            return submit_http_request(request, depth=depth + 1)
        print 'ERROR: {0}'.format(error_code)
        print error.msg
        print error.read()
        exit()


main()
