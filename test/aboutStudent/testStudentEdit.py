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

# TODO name字段值测试
# TODO user_uid字段测试
# TODO number字段测试
# TODO 缺少name 或者 user_uid 或者 number字段

# TODO 编辑后name 重复
# TODO 编辑后number和之前重复,包括和此教师的其他班级中学生number

class StudentEdit(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 班级中创建学生
    def testCreate(self):
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

            # 编辑学生信息
            url = address + '/api/v1/account/student/edit'
            data = {'name': '李思', 'number': '110', 'user_uid': stu_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            # 编辑学生信息
            url = address + '/api/v1/account/student/edit'
            data = {'name': '李思', 'number': '110', 'user_uid': stu_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

