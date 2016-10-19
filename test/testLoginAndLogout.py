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


class LoginAndOutTest(unittest.TestCase):

    # 登录后登出,都成功,最终cookies中去除passport
    def testNormal(self):
        try:
            # login
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
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual('muli', response_json_data['data']['username'])
            self.assertEqual('teacher', response_json_data['data']['role'])
            self.assertEqual('oGEF_wKhg9vaeLBmrtoC3vNAtemY', response_json_data['data']['open_id'])
            self.assertEqual('2016-10-18 11:17:58', response_json_data['data']['time_create'])
            self.assertEqual({}, response_json_data['data']['config'])
            self.assertEqual(0, response_json_data['data']['state_id'])
            self.assertEqual('owzm0w_CXKgVfO4vOWeeBzqL99GI', response_json_data['data']['uid'])
            self.assertTrue('passport' in cookies)

            # logout
            url_logout = address + '/api/v1/account/logout'
            req = urllib2.Request(url_logout)
            content = opener.open(req)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])
            self.assertFalse('passport' in cookies)

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 用户名有误
    def testLoginWrongUser(self):
        try:
            username = '898989898989'
            password = '123123'
            url = address + '/api/v1/account/login'
            data = {'username': username, 'password': password}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response = content.read()
            response_json_data = json.loads(response)
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('Auth Failed', response_json_data['message'])

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 密码有误
    def testLoginWrongPassword(self):
        try:
            username = 'muli'
            password = 'wrongpassword'
            url =  address + '/api/v1/account/login'
            data = {'username': username, 'password': password}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response = content.read()
            response_json_data = json.loads(response)
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('Auth Failed', response_json_data['message'])
        except Exception, e:
            logger.error(e.message)
            self.fail()


    # 用户名为空
    def testLoginEmptyUser(self):
        try:
            password = '123123'
            url = address + '/api/v1/account/login'
            data = {'username': '', 'password': password}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response = content.read()
            response_json_data = json.loads(response)
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('Auth Failed', response_json_data['message'])

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 用户名为空
    def testLoginMissUser(self):
        try:
            username = '898989898989'
            password = '123123'
            url = address + '/api/v1/account/login'
            data = {'password': password}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response = content.read()
            response_json_data = json.loads(response)
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('Auth Failed', response_json_data['message'])

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 密码为空
    def testLoginEmptyUPassword(self):
        try:
            username = 'muli'
            url = address + '/api/v1/account/login'
            data = {'username': username, 'password': ''}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response = content.read()
            response_json_data = json.loads(response)
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('Auth Failed', response_json_data['message'])

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 密码为空
    def testLoginMissPassword(self):
        try:
            username = 'muli'
            url = address + '/api/v1/account/login'
            data = {'username': username}
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response = content.read()
            response_json_data = json.loads(response)
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])
            self.assertEqual('Auth Failed', response_json_data['message'])

        except Exception, e:
            logger.error(e.message)
            self.fail()



    # 连续两次登录,返回code都为0
    def testLoginAndLogin(self):
        try:
            # login
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
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual('muli', response_json_data['data']['username'])
            self.assertEqual('teacher', response_json_data['data']['role'])
            self.assertEqual('oGEF_wKhg9vaeLBmrtoC3vNAtemY', response_json_data['data']['open_id'])
            self.assertEqual('2016-10-18 11:17:58', response_json_data['data']['time_create'])
            self.assertEqual({}, response_json_data['data']['config'])
            self.assertEqual(0, response_json_data['data']['state_id'])
            self.assertEqual('owzm0w_CXKgVfO4vOWeeBzqL99GI', response_json_data['data']['uid'])
            self.assertTrue('passport' in cookies)

            # login
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
            self.assertTrue('passport' in cookies)

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 登录之后连续两次登出,第二次登出code返回2
    def testLoginLogoutAndLogout(self):
        try:
            # login
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
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual('muli', response_json_data['data']['username'])
            self.assertEqual('teacher', response_json_data['data']['role'])
            self.assertEqual('oGEF_wKhg9vaeLBmrtoC3vNAtemY', response_json_data['data']['open_id'])
            self.assertEqual('2016-10-18 11:17:58', response_json_data['data']['time_create'])
            self.assertEqual({}, response_json_data['data']['config'])
            self.assertEqual(0, response_json_data['data']['state_id'])
            self.assertEqual('owzm0w_CXKgVfO4vOWeeBzqL99GI', response_json_data['data']['uid'])
            self.assertTrue('passport' in cookies)

            # logout
            url_logout = address + '/api/v1/account/logout'
            req = urllib2.Request(url_logout)
            content = opener.open(req)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])
            self.assertFalse('passport' in cookies)

            # logout
            url_logout = address + '/api/v1/account/logout'
            req = urllib2.Request(url_logout)
            content = opener.open(req)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual('Passport Error', response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])
            self.assertFalse('passport' in cookies)

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 没有登录直接登出,或者说cookie不含有passport,登出code返回2
    def testLogout(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            url_logout = address + '/api/v1/account/logout'
            req = urllib2.Request(url_logout)
            content = opener.open(req)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual('Passport Error', response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    # passport有误,返回code为2
    def testLogout1(self):
        try:
            url_logout = address + '/api/v1/account/logout'
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', 'passport=wrongpassport'))
            content = opener.open(url_logout)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual('Passport Error', response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    def testLogout2(self):
        try:
            url_logout = address + '/api/v1/account/logout'
            req = urllib2.Request(url_logout)
            content = urllib2.urlopen(req)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual(2, response_json_data['code'])
            self.assertEqual('Passport Error', response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])
        except Exception, e:
            logger.error(e.message)
            self.fail()