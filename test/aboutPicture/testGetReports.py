#encoding:utf-8
import cookielib
import json
import logging
import unittest
import sys
import urllib2
import uuid

import datetime
import requests
import time

from utils.commonMethod import clearCleasses, loginAndCreateClass, my_Login, createExam, clearExams

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}


class GetReports(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    #正常情况, 学生直接上传
    # TODO 用例失败,因为 140257（图片中的学号） 的学号已经创建过
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

            # 查询班级中学生列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            stu_uid = response_json_data['data'][0]['uid']

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

            #获取学生的考试报告
            url = address + '/api/v1/stat/exercise/one/paper?exercise_uid=' + \
                  exam_uid + 'student_uid=' + stu_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

