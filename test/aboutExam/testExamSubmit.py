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


class Examination(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    # 班级中创建学生
    def testNormal(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            loginAndCreateClass(opener)

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

            #编辑考试
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

            #提交考试
            url = address + '/api/v1/exercise/submit'
            data = {'exercise_uid': exam_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            #查看教师考试列表
            url = address + '/api/v1/exercise/list'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(3, response_json_data['data'][0]['status'])
            self.assertEqual(exam_uid, response_json_data['data'][0]['uid'])

            #查看考试信息
            url = address + '/api/v1/exercise/edit?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(3, response_json_data['data']['status'])
            self.assertEqual('内容看这里', response_json_data['data']['origin'][0]['body'].encode('UTF-8'))
            self.assertEqual('标题在这里', response_json_data['data']['origin'][0]['title'].encode('UTF-8'))
            self.assertEqual(100, response_json_data['data']['origin'][0]['number_lower'])
            self.assertEqual(1000, response_json_data['data']['origin'][0]['number_upper'])
            self.assertEqual(150, response_json_data['data']['origin'][0]['score'])

        except Exception, e:
            logger.error(e.message)
            self.fail()