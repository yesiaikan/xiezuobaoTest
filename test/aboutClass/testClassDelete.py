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

from utils.commonMethod import clearCleasses

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'

# TODO 不是此老师创建的能否删除

class ClassCreateTest(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 随机删除多个班级
    def testDeleteManyClasses(self):
        try:
            # 登录
            username = 'muli'
            password = '123123'
            url = address + '/api/v1/account/login'
            data = {'username': username, 'password': password}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            cookies = cookieJar._cookies['pigai.hexinedu.com']['/']
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertTrue('passport' in cookies)

            # 创建10个班级
            uids = []
            for i in range(10):
                url = address + '/api/v1/account/group/edit'
                name = '我的第一个班级_' + str(time.time())
                body = {'name': name}
                data = urllib.urlencode(body)
                request = urllib2.Request(url, data)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                self.assertEqual(200, content.code)
                self.assertEqual(0, response_json_data['code'])
                self.assertEqual(None, response_json_data['message'])
                self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
                uid = response_json_data['data']['uid']
                self.assertIsNotNone(uid)
                uids.append(uid)

            # 随机删除创建的班级
            random.shuffle(uids)
            for uid in uids:
                url = address + '/api/v1/account/group/delete'
                body = {'group_uid': uid}
                data = urllib.urlencode(body)
                request = urllib2.Request(url, data)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                self.assertEqual(200, content.code)
                self.assertEqual(0, response_json_data['code'])
                self.assertEqual(None, response_json_data['message'])
                self.assertEqual(None, response_json_data['data'])

            # 查询教师班级列表
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            datas = response_json_data['data']
            self.assertEqual(0, len(datas))
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #删除时候 错误的uid
    def testDeleteError(self):
        try:
            # 登录
            username = 'muli'
            password = '123123'
            url = address + '/api/v1/account/login'
            data = {'username': username, 'password': password}
            postData = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            cookies = cookieJar._cookies['pigai.hexinedu.com']['/']
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertTrue('passport' in cookies)

            # 创建班级
            url = address + '/api/v1/account/group/edit'
            name = '我的第一个班级_' + str(time.time())
            body = {'name': name}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
            uid = response_json_data['data']['uid']
            self.assertIsNotNone(uid)


            # 删除班级
            url = address + '/api/v1/account/group/delete'
            body = {'group_uid': 'wrongUid'}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertEqual('OB_Group matching query does not exist.', response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])

            # 调用查询教师班级列表接口,没有删除成功
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            datas = response_json_data['data']
            self.assertEqual(1, len(datas))

        except Exception, e:
            logger.error(e.message)
            self.fail()

    #删除时候 缺失group_uid字段,删除失败
    def testDeleteMissGroupUid(self):
        try:
            # 登录
            username = 'muli'
            password = '123123'
            url = address + '/api/v1/account/login'
            data = {'username': username, 'password': password}
            postData = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            cookies = cookieJar._cookies['pigai.hexinedu.com']['/']
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertTrue('passport' in cookies)

            # 创建班级
            url = address + '/api/v1/account/group/edit'
            name = '我的第一个班级_' + str(time.time())
            body = {'name': name}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
            uid = response_json_data['data']['uid']
            self.assertIsNotNone(uid)

            # 删除班级
            url = address + '/api/v1/account/group/delete'
            body = {}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertEqual('OB_Group matching query does not exist.', response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])

            # 调用查询教师班级列表接口,没有删除成功
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            datas = response_json_data['data']
            self.assertEqual(1, len(datas))

        except Exception, e:
            logger.error(e.message)
            self.fail()

    #未登录状态下 delete
    def testDeleteNotLogin(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            url = address + '/api/v1/account/group/delete'
            body = {'group_uid': 'wrongUid'}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual('Passport Error', response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()