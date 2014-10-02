import os
import re
import requests

# add local_settings.py to .gitignore
# variables in local_settings optional, it won't be uploaded
try:
    from local_settings import CLIENT_ID, SECRET_KEY, SHORTCODE
except ImportError:
    CLIENT_ID = None
    SECRET_KEY = None
    SHORTCODE = None

API_URL = 'https://post.chikka.com/smsapi/request'

class Chikka(object):

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def send(self, mobile_number, message, **kwargs):
        payload = self._prepare_payload()

        # check and validate mobile number
        if not mobile_number:
            raise NullMobileNumberException
        else:
            mobile_number = str(mobile_number)

        # e.g. 09991234567
        if len(mobile_number) == 11 and mobile_number.startswith('0'):
            mobile_number = '%s%s' % ('63', mobile_number[1:])

        # e.g. 639991234567
        if not re.match('^63[0-9]{10}', mobile_number):
            raise InvalidMobileNumberException

        payload['mobile_number'] = mobile_number

        # check if request_id was passed to this method
        # means a message was received
        # determines message_type, adds other required payload
        if kwargs.get('request_id') is not None:
            payload['request_id'] = kwargs.get('request_id')

            # if message type is REPLY user is required to supply
            # the request cost
            request_cost = kwargs.get('request_cost')
            if request_cost is not None:
                payload['request_cost'] = request_cost
            else:
                raise NullRequestCostException

            payload['message_type'] = 'REPLY'
        else:
            payload['message_type'] = 'SEND'

        # message_id can be passed to this method
        # this can be useful to track messages sent
        # however if message_id does not exist this method
        # will generate a random message id
        payload['message_id'] = kwargs.get('message_id', 
                                    os.urandom(16).encode('hex'))

        payload['message'] = message

        self.response = requests.post(API_URL, data=payload)

        return payload


    def _prepare_payload(self):
        # check if other required fields exists
        client_id = getattr(self, 'client_id', CLIENT_ID)
        if not client_id:
            print "Error: Your Client ID is required.\n"
            raise NullClientIDException

        secret_key = getattr(self, 'secret_key', SECRET_KEY)
        if not secret_key:
            print "Error: Your Secret Key is required.\n"
            raise NullSecretKeyException

        shortcode = getattr(self, 'shortcode', SHORTCODE)
        if not shortcode:
            print "Error: Your shortcode is required.\n"
            raise NullShortCodeException

        payload = {
            'client_id': client_id,
            'secret_key': secret_key,
            'shortcode': shortcode,
        }

        return payload

# import of exceptions not working on mine
# so placed it here. sorry.
class NullMobileNumberException(Exception):
    pass

class InvalidMobileNumberException(Exception):
    pass

class NullClientIDException(Exception):
    pass

class NullSecretKeyException(Exception):
    pass

class NullShortCodeException(Exception):
    pass

class NullRequestCostException(Exception):
    pass
