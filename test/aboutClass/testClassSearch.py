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


class ClassSearch(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    def testSearchNormal(self):
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
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual(uid, response_json_data['data']['uid'])

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 参数group_uid有误
    def testSearchWrongUid(self):
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

            # 查询班级,查询是否创建成功
            uid = 'wrong_uid'
            url = address + '/api/v1/account/group/edit?group_uid=' + uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            print response_json_data
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('OB_Group matching query does not exist.', response_json_data['message'])

        except Exception, e:
            logger.error(e.message)
            self.fail()


    # TODO 是否需要返回400状态码
    # 缺少参数group_uid
    def testSearchMissUid(self):
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

            # 查询班级,查询是否创建成功
            url = address + '/api/v1/account/group/edit'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            print response_json_data
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('OB_Group matching query does not exist.', response_json_data['message'])

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 未登录状态下查询班级信息
    def testSearchNotLogin(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            url = address + '/api/v1/account/group/edit?group_uid=' + '21214'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual('Passport Error', response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()