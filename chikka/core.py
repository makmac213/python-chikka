import os
import re
import requests

# chikka
from .exceptions import (NullMobileNumberException, NullClientIDException,
                            NullSecretKeyException, NullShortCodeException,
                            InvalidMobileNumberException)

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

        # e.g. 09991234567
        if len(mobile_number) == 11 and mobile_number.startswith('0'):
            mobile_number = '%s%s' % ('63', mobile_number[1:])

        # e.g. 639991234567
        if not re.match('^63[0-9]{10}', mobile_number):
            raise InvalidMobileNumberException

        payload['mobile_number'] = mobile_number

        payload['message'] = message

        payload['message_type'] = 'SEND'

        # message_id can be passed to this method
        # this can be useful to track messages sent
        # however if message_id does not exist this method
        # will generate a random message id
        message_id = kwargs.get('message_id', os.urandom(16).encode('hex'))
        self.message_id = message_id
        payload['message_id'] = message_id

        self.response = requests.post(API_URL, data=payload)


    def _prepare_payload(self):
        # check if other required fields exists
        client_id = getattr(self, 'client_id', None)
        if not client_id:
            raise NullClientIDException

        secret_key = getattr(self, 'secret_key', None)
        if not secret_key:
            raise NullSecretKeyException

        shortcode = getattr(self, 'shortcode', None)
        if not shortcode:
            raise NullShortCodeException

        payload = {
            'client_id': client_id,
            'secret_key': secret_key,
            'shortcode': shortcode,
        }

        return payload

