#encoding:utf-8
import cookielib
import json
import logging
import unittest
import sys
import urllib2

from utils.commonMethod import clearCleasses, loginAndCreateClass

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}

class StudentGetList(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 班级中创建学生
    def testNormal(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)


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

            # 查询班级中学生列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))
        except Exception, e:
            logger.error(e.message)
            self.fail()


    # 缺失参数
    # TODO 缺少班级参数,教师所有学生信息
    def testMissParam(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 查询班级中学生列表
            url = address + '/api/v1/account/student/list'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertTrue(len(response_json_data['data']) >= 0)
        except Exception, e:
            logger.error(e.message)
            self.fail()