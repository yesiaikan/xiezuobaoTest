#encoding:utf-8
import cookielib
import json
import logging
import unittest
import sys
import urllib
import urllib2

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

            # TODO  '' && 前后空格 && None
            nameList = [',/.\`..;:', None, '*&*#@$#%^*!', '  01010110  ', 'normal', '', '0012344']
            for name in nameList:
                # 清空教师班级列表
                clearCleasses()

                # 创建班级
                url = address + '/api/v1/account/group/edit'
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
                # 查询班级列表
                url_grouplist = address + '/api/v1/account/teacher/group'
                request = urllib2.Request(url_grouplist)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                datas = response_json_data['data']
                self.assertEqual(1, len(datas))
                self.assertEqual(name, datas[0]['name'])
                self.assertEqual(uid, datas[0]['uid'])


        except Exception, e:
            logger.error(e.message)
            self.fail()

            # 创建班级名称


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
            self.assertEqual('(1048, "Column \'name\' cannot be null")', response_json_data['message'])

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