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

class StudentDelete(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 删除学生信息
    def testNormal(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0]+'11'
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
                # 创建学生
                url = address + '/api/v1/account/student/batch'
                number = int(str(time.time()).split('.')[0])
                data = {'group_uid': group_uid,
                        'students': [{'name': '张三', 'number': number+i}]}
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
            self.assertEqual(10, len(response_json_data['data']))
            for data in response_json_data['data']:
                stu_uids.append(data['uid'])

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
                # 创建学生
                url = address + '/api/v1/account/student/batch'
                number = int(str(time.time()).split('.')[0])
                data = {'group_uid': group_uid,
                        'students': [{'name': '张三', 'number': number + i}]}
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
            self.assertEqual(10, len(response_json_data['data']))
            for data in response_json_data['data']:
                stu_uids.append(data['uid'])

            #删除
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
            headers = {'Content-Type': 'application/json'}

            # 创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + '12'
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

            # 创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + '13'
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

    # 删除学生信息, user_id列表为空
    def testEmptyUserId(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + '14'
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

            # 删除学生信息
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': group_uid, 'user_uid': []}
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

    #缺失user_uid
    def testMissUserUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + '11'
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

            # 删除学生信息
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': group_uid}
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

    def testMissGroupUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + '11'
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

            # 删除学生信息
            url = address + '/api/v1/account/group/student/quit'
            data = {'user_uid': [stu_uid]}
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

    def testWrongGroupUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + '11'
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

            # 删除学生信息
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': 'wrong', 'user_uid': [stu_uid]}
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

