#encoding:utf-8
import cookielib
import json
import logging
import unittest
import sys
import urllib2
import uuid

import requests
import time

from utils.commonMethod import clearCleasses, loginAndCreateClass, my_Login, createExam, clearExams

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}


class CantNotRead(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    #正常情况,
    def testCanRead(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': '140257'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            #上传图片
            url = address + '/api/v1/pool/image/access?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            accessid = response_json_data['data']['accessid']
            url = response_json_data['data']['host']
            expire = response_json_data['data']['expire']
            signature = response_json_data['data']['signature']
            policy = response_json_data['data']['policy']
            dir = response_json_data['data']['dir']
            filename = uuid.uuid4().hex + '-origin.jpg'
            data = {'name': str(filename), 'key': str(dir) + filename, 'policy': str(policy),
                    'signature': str(signature), 'OSSAccessKeyId': str(accessid)}
            files = {'file': open('test.jpg', 'rb')}
            resp = requests.post(url, data=data, files=files)
            self.assertEqual(204, resp.status_code)

            time.sleep(1)
            #开始处理
            url = address + '/api/v1/pool/image/access'
            data = {'uid': filename.split('-')[0], 'exercise_uid': exam_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            time.sleep(5)
            #获取未识别的图片
            url = address + '/api/v1/pool/image/student?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #没有此学号信息,图片不能识别
    def testReadWithWrongNumber(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            #上传图片
            url = address + '/api/v1/pool/image/access?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            accessid = response_json_data['data']['accessid']
            url = response_json_data['data']['host']
            expire = response_json_data['data']['expire']
            signature = response_json_data['data']['signature']
            policy = response_json_data['data']['policy']
            dir = response_json_data['data']['dir']
            filename = uuid.uuid4().hex + '-origin.jpg'
            data = {'name': str(filename), 'key': str(dir) + filename, 'policy': str(policy),
                    'signature': str(signature), 'OSSAccessKeyId': str(accessid)}
            files = {'file': open('test.jpg', 'rb')}
            resp = requests.post(url, data=data, files=files)
            self.assertEqual(204, resp.status_code)

            time.sleep(1)
            #开始处理
            url = address + '/api/v1/pool/image/access'
            data = {'uid': filename.split('-')[0], 'exercise_uid': exam_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            time.sleep(15)
            #获取未识别的图片
            url = address + '/api/v1/pool/image/student?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual(3, response_json_data['data'][0]['status'])
            self.assertIsNotNone(response_json_data['data'][0]['anchors'])
            self.assertIsNotNone(response_json_data['data'][0]['url'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 图片不能识别
    # 上传错误图片  开始处理 获取未识别图片
    def testReadWithoutNumber(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            # 上传图片
            url = address + '/api/v1/pool/image/access?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            accessid = response_json_data['data']['accessid']
            url = response_json_data['data']['host']
            expire = response_json_data['data']['expire']
            signature = response_json_data['data']['signature']
            policy = response_json_data['data']['policy']
            dir = response_json_data['data']['dir']
            filename = uuid.uuid4().hex + '-origin.jpg'
            data = {'name': str(filename), 'key': str(dir) + filename, 'policy': str(policy),
                    'signature': str(signature), 'OSSAccessKeyId': str(accessid)}
            files = {'file': open('test_wrong.jpg', 'rb')}
            resp = requests.post(url, data=data, files=files)
            self.assertEqual(204, resp.status_code)

            time.sleep(1)
            # 开始处理
            url = address + '/api/v1/pool/image/access'
            data = {'uid': filename.split('-')[0], 'exercise_uid': exam_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertIsNotNone(response_json_data['data']['url'])
            self.assertIsNotNone(response_json_data['data']['id'])

            time.sleep(5)
            # 获取未识别的图片
            url = address + '/api/v1/pool/image/student?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual(3, response_json_data['data'][0]['status'])
            self.assertIsNotNone(response_json_data['data'][0]['anchors'])
            self.assertIsNotNone(response_json_data['data'][0]['url'])
        except Exception, e:
            logger.error(e.message)
            self.fail()


    #缺少参数
    def testMissexam_uid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            createExam(opener)
            url = address + '/api/v1/pool/image/student'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #错误参数
    def testWrongexam_uid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            createExam(opener)
            url = address + '/api/v1/pool/image/student?exercise_uid=' + 'wrong'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #错误参数
    def testWrongexam_uid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            createExam(opener)
            url = address + '/api/v1/pool/image/student?exercise_uid=' + ''
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()