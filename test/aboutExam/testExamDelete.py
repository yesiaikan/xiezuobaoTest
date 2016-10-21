#encoding:utf-8
import cookielib
import json
import logging
import random
import unittest
import sys
import urllib
import urllib2

from utils.commonMethod import clearCleasses, loginAndCreateClass, clearExams

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}

# subject 为 chinese,math,english,physics,chemistry,biology,history,geography,phlitics,others

class Examination(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    def testDelete(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            loginAndCreateClass(opener)

            # 查看教师考试列表
            url = address + '/api/v1/exercise/list'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            datas = response_json_data['data']
            for data in datas:
                exam_uid = data['uid']
                url = address + '/api/v1/exercise/delete'
                data = {'exercise_uid': exam_uid}
                postData = json.dumps(data)
                request = urllib2.Request(url, postData, headers)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                self.assertEqual(200, content.code)
                self.assertEqual(0, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()