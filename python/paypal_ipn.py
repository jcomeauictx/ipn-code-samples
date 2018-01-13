#!/usr/bin/python
'''
This module processes PayPal Instant Payment Notification messages (IPNs).
'''
from __future__ import print_function

import sys
import cgi
import smtplib
import logging

try:  # Python2
    import urlparse
    from urllib2 import Request, urlopen
    from urllib import urlencode
except ImportError:  # Python3
    import urllib.parse as urlparse
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode

VERIFY_URL_PROD = 'https://www.paypal.com/cgi-bin/webscr'
VERIFY_URL_TEST = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)
logging.debug('logging at DEBUG level')

def paypal_ipn(verify_url=VERIFY_URL_TEST):
    '''
    verify PayPal transaction
    '''
    print('content-type: text/plain', end='\r\n\r\n')
    parameters = urlparse.parse_qsl(sys.stdin.read())
    # Add '_notify-validate' parameter
    parameters.append(('cmd', '_notify-validate'))
    postdata = urlencode(dict(parameters)).encode('utf8')
    logging.info('postdata: %s', postdata)
    request = Request(verify_url)
    request.add_header('content-type', 'application/x-www-form-urlencoded')
    # Post back to PayPal for validation
    logging.info('posting to %s', verify_url)
    response = urlopen(request, postdata).read().decode('utf8')
    logging.info('response: %s', response)
    if response == 'VERIFIED':
        logging.info('valid transaction')
    elif response == 'INVALID':
        logging.warning('invalid transaction')
    else:
        logging.error('unexpected response: %s', response)

if __name__ == '__main__':
    paypal_ipn()
