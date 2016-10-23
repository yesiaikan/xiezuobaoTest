#encoding:utf-8
import cookielib
import json
import logging
import random
import unittest
import sys
import urllib
import urllib2

import time

from utils.commonMethod import clearCleasses, loginAndCreateClass

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}

# TODO 老师不同班级中创建 编辑 删除学生操作 校验
# TODO 删除其他班级的学生,是否可行

class StudentCreate(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 班级中创建学生
    def testCreate(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            #创建学生
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
            self.assertEqual(0, len(response_json_data['data']))

            #学生列表获取学生uid
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual('张三', response_json_data['data'][0]['name'].encode('UTF-8'))
            self.assertEqual(number, response_json_data['data'][0]['number'])
            stu_uid = response_json_data['data'][0]['uid']


            # 编辑学生信息    TODO 编辑有问题
            url = address + '/api/v1/account/student/edit'
            data = {'name': '李思', 'number': number, 'user_uid': stu_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            # 获取学生信息
            url = address + '/api/v1/account/student/edit?student_uid=' + stu_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual('李思', response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual('student', response_json_data['data']['role'])
            stu_uid_1 = response_json_data['data']['uid']
            self.assertEqual(stu_uid, stu_uid_1)

            # 查询班级中学生列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual('李思', response_json_data['data'][0]['name'].encode('UTF-8'))
            self.assertEqual(number, response_json_data['data'][0]['number'])
            self.assertEqual(stu_uid, response_json_data['data'][0]['uid'])

            # 删除学生信息
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': group_uid, 'user_uid': [stu_uid]}
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
            self.assertEqual(0, len(response_json_data['data']))
        except Exception, e:
            logger.error(e.message)
            self.fail()

