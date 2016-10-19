#encoding:utf-8
import cookielib
import json
import logging
import unittest
import sys
import urllib
import urllib2

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'


class GetUserInfoTest(unittest.TestCase):

    # 登录状态下获取用户信息
    def testNormal(self):
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

            # 获取用户信息
            url_userinfo = address + '/api/v1/account/own'
            request = urllib2.Request(url_userinfo)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual('muli', response_json_data['data']['username'])
            self.assertEqual('teacher', response_json_data['data']['role'])
            self.assertEqual('oGEF_wKhg9vaeLBmrtoC3vNAtemY', response_json_data['data']['open_id'])
            self.assertEqual('2016-10-18 11:17:58', response_json_data['data']['time_create'])
            self.assertEqual({}, response_json_data['data']['config'])
            self.assertEqual(0, response_json_data['data']['state_id'])
            self.assertEqual('owzm0w_CXKgVfO4vOWeeBzqL99GI', response_json_data['data']['uid'])
            self.assertEqual(None, response_json_data['data']['state'])

        except Exception, e:
            logger.error(e.message)
            self.fail()


    # 不在登录状态下,直接获取用户信息
    def testNotLogin(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            url_userinfo = address + '/api/v1/account/own'
            request = urllib2.Request(url_userinfo)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('Passport Error', response_json_data['message'])
        except Exception, e:
            logger.error(e.message)
            self.fail()



    # 登出后获取用户信息
    def testLoginout(self):
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

            # 登出
            url_logout = address + '/api/v1/account/logout'
            req = urllib2.Request(url_logout)
            content = opener.open(req)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertFalse('passport' in cookies)

            # 获取用户信息
            url_userinfo = address + '/api/v1/account/own'
            request = urllib2.Request(url_userinfo)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('Passport Error', response_json_data['message'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

