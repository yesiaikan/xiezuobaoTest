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


class GetReportPaper(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    def testWrongStudentUid(self):
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


            #获取学生的考试报告
            url = address + '/api/v1/stat/exercise/one/paper?exercise_uid=' + \
                  exam_uid + '&student_uid=' + 'wrong'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertIsNone(response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()


    #exam_uid参数有误
    def testWrongExamUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0]
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张三', 'number': number + '0'}]}
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

            # 获取学生的考试报告
            url = address + '/api/v1/stat/exercise/one/paper?exercise_uid=' + \
                  'wrong' + '&student_uid=' + stu_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertIsNone(response_json_data['data'])


        except Exception, e:
            logger.error(e.message)
            self.fail()


    # exam_uid参数缺少
    def testMissExamUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0]
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张三', 'number': number + '0'}]}
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

            # 获取学生的考试报告
            url = address + '/api/v1/stat/exercise/one/paper?student_uid=' + stu_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertIsNone(response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()


    # exam_uid参数有误
    def testWrongStudentUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0]
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张三', 'number': number + '0'}]}
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

            # 获取学生的考试报告
            url = address + '/api/v1/stat/exercise/one/paper?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertIsNone(response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()
