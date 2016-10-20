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

# TODO user_uid参数测试,包括缺失参数
# TODO group_uid参数测试,包括缺失参数

class StudentDelete(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 删除学生信息
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

    #随机删除学生, 每次删除一个
    def testDeleteSingle(self):
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
            for stu_uid in stu_uids:            # 删除学生信息
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

    # 随机删除多个学生, 1次删完
    def testDeleteBatch(self):
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
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': group_uid, 'user_uid': stu_uids}
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

    # 填写其他班级的group_uid, 不应该能删除成功
    def testOtherGroupUID(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/edit'
            data = {'name': '张三', 'number': '001', 'group_uid': group_uid}
            postData = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual('张三', response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual('student', response_json_data['data']['role'])
            stu_uid = response_json_data['data']['uid']
            self.assertIsNotNone(stu_uid)

            # 创建其他班级
            url = address + '/api/v1/account/group/edit'
            name = '其他班级'
            body = {'name': name}
            data = json.dumps(body)
            headers = {'Content-Type': 'application/json'}
            request = urllib2.Request(url, data, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual(name.strip(), response_json_data['data']['name'].encode('UTF-8'))
            other_group_uid = response_json_data['data']['uid']
            self.assertIsNotNone(other_group_uid)

            # 删除学生信息, 删除学生失败
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': other_group_uid, 'user_uid': [stu_uid]}
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
        except Exception, e:
            logger.error(e.message)
            self.fail()


    # 填写的group_uid有误, 不应该能删除成功
    def testWrongGroupUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/edit'
            data = {'name': '张三', 'number': '001', 'group_uid': group_uid}
            postData = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual('张三', response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual('student', response_json_data['data']['role'])
            stu_uid = response_json_data['data']['uid']
            self.assertIsNotNone(stu_uid)


            # 删除学生信息, 删除学生失败
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': 'wrong_group_uid', 'user_uid': [stu_uid]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])

            # 查询班级中学生列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
        except Exception, e:
            logger.error(e.message)
            self.fail()
