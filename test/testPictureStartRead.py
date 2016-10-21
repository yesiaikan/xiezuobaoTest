#encoding:utf-8
import cookielib
import json
import logging
import unittest
import sys
import urllib2
import uuid

import requests

from utils.commonMethod import clearCleasses, loginAndCreateClass, my_Login, createExam, clearExams

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}

# TODO 开始处理图片的uid exercise_uid student_uid字段测试; student_uid可选行已测

class Read(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    #上传图片后  开始处理
    def testStart(self):
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

            #开始处理
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
        except Exception, e:
            logger.error(e.message)
            self.fail()


    # 处理的图片 和 考试信息不对应
    def testStartWrongExamUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            url = address + '/api/v1/pool/image/access'
            data = {'uid': 'muli', 'exercise_uid': exam_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 上传图片后携带学生信息
    def testWithRightStuUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/edit'
            data = {'name': '张三', 'number': '001', 'group_uid': group_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual('张三', response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual('student', response_json_data['data']['role'])
            stu_uid = response_json_data['data']['uid']
            self.assertIsNotNone(stu_uid)

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

            #开始处理
            url = address + '/api/v1/pool/image/access'
            data = {'uid': filename.split('-')[0], 'exercise_uid': exam_uid, 'student_uid': stu_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertIsNotNone(response_json_data['data']['url'])
            self.assertIsNotNone(response_json_data['data']['id'])
        except Exception, e:
            logger.error(e.message)
            self.fail()


    #上传图片后携带学生信息有误
    def testWithWrongStuUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

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


            url = address + '/api/v1/pool/image/access'
            data = {'uid': filename.split('-')[0], 'exercise_uid': exam_uid, 'student_uid':'123'}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertEqual('US_User matching query does not exist.', response_json_data['message'])
        except Exception, e:
            logger.error(e.message)
            self.fail()