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

class ClassCreateTest(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 创建班级的 name 字段测试
    def testCreate(self):
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

            nameList = [',/.\`..;:', '*&*#@$#%^*!', '  01010110  ', 'normal', '0012344']
            for name in nameList:
                # 清空教师班级列表
                clearCleasses()

                # 创建班级
                url = address + '/api/v1/account/group/edit'
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
                uid = response_json_data['data']['uid']
                self.assertIsNotNone(uid)

                # 查询班级,查询是否创建成功
                # 查询班级列表
                url_grouplist = address + '/api/v1/account/teacher/group'
                request = urllib2.Request(url_grouplist)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                datas = response_json_data['data']
                self.assertEqual(1, len(datas))
                self.assertEqual(name.strip(), datas[0]['name'])
                self.assertEqual(uid, datas[0]['uid'])
        except Exception, e:
            logger.error(e.message)
            self.fail()


    #创建班级时候name测试
    def testCreateError(self):
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

            # TODO  '' && 前后空格 && None
            nameList = ['  ', None, '']
            for name in nameList:
                # 清空教师班级列表
                clearCleasses()

                # 创建班级
                url = address + '/api/v1/account/group/edit'
                body = {'name': name}
                data = json.dumps(body)
                headers = {'Content-Type': 'application/json'}
                request = urllib2.Request(url, data, headers)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                self.assertEqual(200, content.code)
                self.assertEqual(1, response_json_data['code'])
                self.assertEqual(None, response_json_data['data'])

                # 查询班级,查询是否创建成功
                url_grouplist = address + '/api/v1/account/teacher/group'
                request = urllib2.Request(url_grouplist)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                datas = response_json_data['data']
                self.assertEqual(0, len(datas))
        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 创建班级时缺少name字段
    def testCreateMissName(self):
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
            body = {}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])

            # 查询班级,查询是否创建成功
            # 查询班级列表
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            datas = response_json_data['data']
            self.assertEqual(0, len(datas))

        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 未登录状态下创建班级
    def testCreateNotLogin(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            url = address + '/api/v1/account/group/edit'
            body = {}
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

    #连续创建同名子班级
    def testCreateSameNameClasses(self):
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

            uids = []
            for i in range(10):
                # 创建班级
                url = address + '/api/v1/account/group/edit'
                name = '同样名字吧' + str(time.time())
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

            random.shuffle(uids)
            # 查询教师班级列表
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            datas = response_json_data['data']
            self.assertEqual(len(uids), len(datas))
            for i in range(len(uids)):
                self.assertTrue('同样名字吧' in datas[int(i)]['name'].encode('UTF-8'))
        except Exception, e:
            logger.error(e.message)
            self.fail()
