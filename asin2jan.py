#!/opt/local/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import re
import urllib

import argparse
from pit import Pit
ACCESS_KEY = Pit.get('Amazon')['AWSAccessKeyId']
SECRET_KEY = Pit.get('Amazon')['AWSSecretAccessKeyId']

def main():
    args = parse_args()
    # print args
    sys.stdout.write(getjan(args.asin)) 
    if not args.n:
        sys.stdout.write(os.linesep) 

def parse_args():
    p = argparse.ArgumentParser("ASIN to JAN/ESN converter")
    p.add_argument('-n', action='store_true', default=False)
    p.add_argument('asin', type=str)
    return p.parse_args()

def getjan(asin):
    url = 'http://ecs.amazonaws.com/onca/xml'
    params = {
            'Service': 'AWSECommerceService', 
            'AWSAccessKeyId': ACCESS_KEY, 
            # アソシエイトタグは必須項目なので、適当な名前を入れる
            'AssociateTag': 'Unknown', 
            'Operation': 'ItemLookup', 
            'ItemId': asin, 
            'ResponseGroup': 'ItemAttributes', 
            }
    url = get_signed_url(url, params)
    res = urllib.urlopen(url).read()
    if not res:
        raise 'no results'
    # print res
    try:
        return re.findall(r'<EAN>([^<]+)', res)[0]
    except:
        return None

def test():
    print getjan('B005119CMA')

def get_signed_url(url, params):
    import hmac
    import hashlib
    import base64
    from urlparse import urlparse
    import time

    url = urlparse(url)
    string_to_sign = 'GET\n%s\n%s\n' % (url.netloc, url.path)
    
    params.update({
        'Version': '2009-04-15', 
        'SignatureVersion': '2', 
        'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()), 
        'SignatureMethod': 'HmacSHA256', 
        })

    keys = params.keys()
    keys.sort()
    pairs = []
    for key in keys:
        val = params[key]
        pairs.append(urllib.quote(key, safe='') + '=' + urllib.quote(val, safe='-_~'))
    qs = '&'.join(pairs)
    string_to_sign += qs
    
    sig = base64.b64encode(hmac.new(SECRET_KEY, string_to_sign, hashlib.sha256).digest())
    url = "%s?%s&Signature=%s" % (url.geturl(), qs, urllib.quote(sig))
    return url

if __name__  == '__main__':
    main()

