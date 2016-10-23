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

import datetime

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
# TODO 编辑后number和之前重复,包括和此教师的其他班级中学生number

class StudentEdit(unittest.TestCase):

    def setUp(self):
        clearCleasses()
    #TODO 存再bug   编辑返回code为2
    def testNormal(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + str(datetime.datetime.now().microsecond)
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))

            # 学生列表获取学生uid
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

            # 编辑学生信息
            url = address + '/api/v1/account/student/edit'
            data = {'name': '李思', 'number': number, 'user_uid': stu_uid}
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
            self.assertEqual('李思', response_json_data['data'][0]['name'].encode('UTF-8'))
            self.assertEqual('110', response_json_data['data'][0]['number'])
            self.assertEqual(stu_uid, response_json_data['data'][0]['uid'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #随机编辑多个学生
    def testEditManyRandom(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            stu_uids = []
            for i in range(10):
                # 班级中创建学生
                url = address + '/api/v1/account/student/edit'
                data = {'name': '张三', 'number': str(i), 'group_uid': group_uid}
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
                stu_uids.append(stu_uid)

            random.shuffle(stu_uids)
            i = 10
            for stu_uid in stu_uids:
                # 编辑学生信息
                url = address + '/api/v1/account/student/edit'
                data = {'name': '李思', 'number': str(i), 'user_uid': stu_uid}
                postData = json.dumps(data)
                request = urllib2.Request(url, postData, headers)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                self.assertEqual(200, content.code)
                self.assertEqual(0, response_json_data['code'])
                i += 1

            # 查询班级中学生列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(10, len(response_json_data['data']))
            total = 0
            for i in range(10):
                self.assertEqual('李思', response_json_data['data'][i]['name'].encode('UTF-8'))
                total += int(response_json_data['data'][i]['number'])
                self.assertTrue(int(response_json_data['data'][i]['number']) >= 10)
                self.assertTrue(response_json_data['data'][i]['uid'] in stu_uids)
            self.assertEqual(145, total)
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #编辑后学号重复
    def testToSameNumber(self):
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

            # 班级中创建学生
            url = address + '/api/v1/account/student/edit'
            data = {'name': '张三', 'number': '002', 'group_uid': group_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual('张三', response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual('student', response_json_data['data']['role'])
            stu_uid1 = response_json_data['data']['uid']
            self.assertIsNotNone(stu_uid1)

            # 编辑学生信息 TODO 编辑后学号重复, 不应该编辑成功
            url = address + '/api/v1/account/student/edit'
            data = {'name': '李思', 'number': '002', 'user_uid': stu_uid}
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
            self.assertEqual('李思', response_json_data['data'][0]['name'].encode('UTF-8'))
            self.assertEqual('110', response_json_data['data'][0]['number'])
            self.assertEqual(stu_uid, response_json_data['data'][0]['uid'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

