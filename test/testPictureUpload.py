#encoding:utf-8
import cookielib
import json
import logging
import random
import unittest
import sys
import urllib
import urllib2

from utils.commonMethod import clearCleasses, loginAndCreateClass

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}


class StudentCreate(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 班级中创建学生
    def testCreate(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 创建考试
            url = address + '/api/v1/exercise/edit'
            name = '考试啦'
            subject = 'chinese'
            data = {'name': name, 'subject': subject, 'manual': True}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
            # self.assertEqual(subject, response_json_data['data']['subject'])
            exam_uid = response_json_data['data']['uid']
            self.assertIsNotNone(exam_uid)

            # 编辑考试
            url = address + '/api/v1/exercise/edit'
            name = '考试啦'
            data = {'name': name, 'exercise_uid': exam_uid,
                    'origin': [{'body': '内容看这里', 'doi': 1, 'title': '标题在这里', 'answer': '',
                                'number_upper': 1000, 'number_lower': 100, 'score': 150}]
                    }
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            # 提交考试
            url = address + '/api/v1/exercise/submit'
            data = {'exercise_uid': exam_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            url = address + '/api/v1/pool/image/access?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)

        except Exception, e:
            logger.error(e.message)
            self.fail()

