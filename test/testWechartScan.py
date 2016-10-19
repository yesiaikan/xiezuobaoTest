#encoding:utf-8
import cookielib
import json
import logging
import unittest
import sys
import urllib
import urllib2

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'


class WechartScanTest(unittest.TestCase):

    def testNormal(self):
        url = address + '/api/v1/account/wechat/qrcode'
        params = {"is_pigai": "pigai", "code": 23423423}
        req = urllib2.Request(url, data=urllib.urlencode(params))
        content = urllib2.urlopen(req)
        response_json_data = json.loads(content.read())
        print response_json_data



