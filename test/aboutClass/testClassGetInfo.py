#encoding:utf-8
import cookielib
import json
import logging
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


class ClassesGetInfoTest(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    def testGetInfoNoraml(self):
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

            # 查询班级,查询是否创建成功
            url = address + '/api/v1/account/group/edit?group_uid=' + uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            print response_json_data
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual(uid, response_json_data['data']['uid'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    def testMissGroupUid(self):
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

            # 查询班级,查询是否创建成功
            url = address + '/api/v1/account/group/edit'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            print response_json_data
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    def testWrongGroupUid(self):
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

            # 查询班级,查询是否创建成功
            url = address + '/api/v1/account/group/edit?group_uid=' + 'wrongGroupUid'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            print response_json_data
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()