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


class ClassesTest(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    def testAllAboutClass(self):
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

            # 编辑班级,修改名称
            url = address + '/api/v1/account/group/edit'
            name = '我的第一个班级改名了' + str(time.time())
            body = {'name': name, 'group_uid': uid}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])

            # 查询班级,查询名称是否修改
            url = address + '/api/v1/account/group/edit?group_uid=' + uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual(uid, response_json_data['data']['uid'])

            # 删除班级
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

            # 查询班级,班级没有真正删除,此接口查询结果不变
            url = address + '/api/v1/account/group/edit?group_uid=' + uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
            self.assertEqual(uid, response_json_data['data']['uid'])

            #调用查询教师班级列表接口,查询结果中data为空
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            datas = response_json_data['data']
            self.assertEqual(0, len(datas))

        except Exception, e:
            logger.error(e.message)
            self.fail()


    def testClearClass(self):
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

            # 查询班级列表
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            datas = response_json_data['data']

            # 如果班级列表不为空,则删除
            if datas:
                for obj in datas:
                    uid = obj['uid']
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


        except Exception, e:
            logger.error(e.message)
            self.fail()