"""
Despite being a bit verbose, this is a good example of who to use suds to call the Execute2 method.
"""

import logging
from suds.client import Client

KEY = file('key.txt').read()
SUDS_CLIENT = 'suds.client'
SERVICE_URL = 'https://api.qualifiedAddress.com/Address/v1/VerifyService.asmx?wsdl'
ADDRESS_INCOMPLETE = 'ERROR: Address is not complete, not verifying.'
QAD_DOWN = 'ERROR: QA Server error: '
BAD_ADDRESS = 'ERROR: Address could not be verified.'


class LiveAddressService(object):
    def __init__(self, suggestions=10, sandbox=False, logging=False):
        self.sandbox = sandbox
        if logging: self._enable_logging()
        self.client = Client(SERVICE_URL)
        self.suggestions = suggestions

    def _enable_logging(self):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(SUDS_CLIENT).setLevel(logging.DEBUG)
        
    def verify_address(self, address):
        if not address.is_complete():
            return LiveAddressResponse(success=False, qualified_addresses=[address], message=ADDRESS_INCOMPLETE)

        result = self._get_raw_result(address)
        
        if not result.Success:
            return LiveAddressResponse(verified=False, qualified_addresses=[address], message=QAD_DOWN + result.Message)

        if len(result.Addresses.ArrayOfAddressResponse) < 1:
            return LiveAddressResponse(verified=False, qualified_addresses=[address], message=BAD_ADDRESS)
 
        return LiveAddressResponse(verified=True, qualified_addresses=self._package_result_addresses(result))

    def _get_raw_result(self, address):
        request = dict(sandbox=self.sandbox, key=KEY, suggestions=self.suggestions, addressee='', 
            street=address.street1, street2=address.street2, city=address.city, state=address.state,
            zipCode=address.zipcode, lastLine=address.last_line, unitNumber='', urbanization='')
        
        return self.client.service.Execute2(**request)
    
    def _package_result_addresses(self, result):
        return [QualifiedAddress(a['Street'], a['Street2'], a['City'], a['State'], a['ZipCode']) 
            for a in result.Addresses.ArrayOfAddressResponse[0].AddressResponse]


TAB = '\n    '
DOUBLE_TAB = '\n        '

class LiveAddressResponse(object):
    def __init__(self, verified=False, qualified_addresses=None, message=''):
        self.verified = verified
        self.addresses = qualified_addresses or []
        self.message = message
        
    def __repr__(self):
        formatted_addresses = ''.join([DOUBLE_TAB + repr(address) for address in self.addresses])
        rep = 'LiveAddressResponse('
        rep += TAB + 'verified={0},'.format(self.verified)
        rep += TAB + 'qualified_addresses=[{0}'.format(formatted_addresses)
        rep += TAB + '],'
        rep += TAB + 'message="{0}"'.format(self.message)
        rep += '\n)'
        return rep


class QualifiedAddress(object):
    def __init__(self, street, street2, city, state, zipcode):
        self.street = street + '\n{0}'.format(street2) if street2 else street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        
    def __str__(self):
        return '{0}\n{1}, {2} {3}'.format(self.street, self.city, self.state, self.zipcode)
    
    def __repr__(self):
        return 'QualifieldAddress(street="{0}", city="{1}", state="{2}", zipcode="{3}")'\
            .format(self.street, self.city, self.state, self.zipcode)
        
        
class InputAddress(object):
    def __init__(self, street1="", street2="", city="", state="", zipcode=""):
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.last_line = self._last_line()
            
    def is_complete(self):
        return self.street1 and (
            self.zipcode or
            self.city or
            (self.city and self.state))
            
    def _last_line(self):
        return '{0}, {1} {2}'.format(self.city, self.state, str(self.zipcode))
        
    def __repr__(self):
        return "InputAddress(street1='{0}', street2='{1}', city='{2}', state='{3}', zipcode='{4}')"\
            .format(self.street1, self.street2, self.city, self.state, self.zipcode)


if __name__ == '__main__':
    address = InputAddress(street1='100', city='new york', state='NY')

    print
    print address
    print 

    print
    print LiveAddressService().verify_address(address)
    print 
