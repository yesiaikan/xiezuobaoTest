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


class SignToStudent(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    #没有此序号信息,图片不能识别  之后标记到学生
    def testSignToStu1(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0]
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            #获取创建学生的id
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
            data = {'name': filename, 'key': dir + filename, 'policy': policy,
                    'signature': signature, 'OSSAccessKeyId': accessid}
            files = {'file': open('test_wrong.jpg', 'rb')}
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
            self.assertIsNotNone(response_json_data['data'][0]['id'])
            pic_id = response_json_data['data'][0]['id']

            #获取考试提交进度
            url = address + '/api/v1/stat/exercise/student/process?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(3, response_json_data['data'][0]['status'])

            #标记到学生
            url = address + '/api/v1/pool/image/student'
            data = {'id': pic_id, 'exercise_uid': exam_uid, 'student_uid': stu_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            #获取考试提交进度  全部识别完成
            time.sleep(5)
            url = address + '/api/v1/stat/exercise/student/process?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(6, response_json_data['data'][0]['status'])
        except Exception, e:
            logger.error(e.message)
            self.fail()




    # 没有此序号信息,图片不能识别  之后标记到其中一个学生
    def testSignToStu2(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0]
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张三', 'number': number+'0'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            # 获取创建学生的id
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(2, len(response_json_data['data']))
            stu_uid = response_json_data['data'][0]['uid']
            stu_uid1 = response_json_data['data'][1]['uid']


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
            data = {'name': filename, 'key': dir + filename, 'policy': policy,
                    'signature': signature, 'OSSAccessKeyId': accessid}
            files = {'file': open('test_wrong.jpg', 'rb')}
            resp = requests.post(url, data=data, files=files)
            self.assertEqual(204, resp.status_code)

            # 开始处理
            time.sleep(1)
            url = address + '/api/v1/pool/image/access'
            data = {'uid': filename.split('-')[0], 'exercise_uid': exam_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            time.sleep(15)
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
            self.assertIsNotNone(response_json_data['data'][0]['id'])
            pic_id = response_json_data['data'][0]['id']

            # 获取考试提交进度
            url = address + '/api/v1/stat/exercise/student/process?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(3, response_json_data['data'][0]['status'])

            # 标记到学生
            url = address + '/api/v1/pool/image/student'
            data = {'id': pic_id, 'exercise_uid': exam_uid, 'student_uid': stu_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            # 获取考试提交进度  全部识别完成, 只统计上传过图片的
            time.sleep(5)
            url = address + '/api/v1/stat/exercise/student/process?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(6, response_json_data['data'][0]['status'])
            self.assertEqual(stu_uid, response_json_data['data'][0]['uid'])

            #获取学生的考试报告
            url = address + '/api/v1/stat/exercise/one/paper?exercise_uid=' + \
                  exam_uid + 'student_uid=' + stu_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertIsNotNone(response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()