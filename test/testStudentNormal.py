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

# TODO 老师不同班级中创建 编辑 删除学生操作 校验
# TODO 针对每个用到的学生操作接口进行测试
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
            self.assertEqual('110', response_json_data['data'][0]['number'])
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

    # 批量创建学生
    # TODO 上述bug修复后,添加此用例:  学号不重复不一定在一个班内，一个老师教的学生都不应该重复，测试的时候得注意
    def testCreateAsList(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid, 'students': [{'name': '张三', 'number': '001'}, {'name': '张四', 'number': '199'}, {'name': '张五', 'number': '001'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual('001', response_json_data['data'][0]['number'])
            self.assertEqual('张五', response_json_data['data'][0]['name'].encode('UTF-8'))

        except Exception, e:
            logger.error(e.message)
            self.fail()

    #创建学号和之前创建的学号重复
    def testCreateSameNumber(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': '001'}, {'name': '张四', 'number': '199'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))


            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid,
                    'students': [{'name': '赵柳', 'number': '008'},
                                 {'name': '赵柳', 'number': '009'},
                                 {'name': '嫦娥', 'number': '009'},
                                 {'name': '李磊', 'number': '001'},
                                 {'name': '李明', 'number': '199'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(3, len(response_json_data['data']))

        except Exception, e:
            logger.error(e.message)
            self.fail()