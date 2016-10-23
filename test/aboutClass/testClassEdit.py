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

class ClassEditTest(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 修改名称,改了又改
    def testEdit(self):
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

            # 编辑班级,修改名称
            url = address + '/api/v1/account/group/edit'
            name = '我的第一个班级又改名了' + str(time.time())
            body = {'name': name, 'group_uid': uid}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])

            #查询教师班级列表
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            datas = response_json_data['data']
            self.assertEqual(1, len(datas))
            self.assertEqual(name, datas[0]['name'].encode('UTF-8'))
            self.assertEqual(uid, datas[0]['uid'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #未登录状态下进行edit修改操作
    def testEditNotLogin(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            url = address + '/api/v1/account/group/edit'
            name = '我的第一个班级改名了' + str(time.time())
            uid = '111234'
            body = {'name': name, 'group_uid': uid}
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


    # 测试edit的参数   TODO '   '
    def testEditName(self):
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

            # 编辑班级,修改名称
            nameList = [name, ',/.\`..;:', '*&*#@$#%^*!', '  01010110  ', '000909900000', 'normal', None, '', '   ']
            for name in nameList:
                url = address + '/api/v1/account/group/edit'
                body = {'name': name, 'group_uid': uid}
                data = json.dumps(body)
                headers = {'Content-Type': 'application/json'}
                request = urllib2.Request(url, data, headers)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                self.assertEqual(200, content.code)
                self.assertEqual(0, response_json_data['code'])
                self.assertEqual(None, response_json_data['message'])
                self.assertEqual(None, response_json_data['data'])

                if name and name.strip() is not '':
                    # 查询教师班级列表
                    temp_name = name
                    url_grouplist = address + '/api/v1/account/teacher/group'
                    request = urllib2.Request(url_grouplist)
                    content = opener.open(request)
                    response_json_data = json.loads(content.read())
                    datas = response_json_data['data']
                    self.assertEqual(1, len(datas))
                    self.assertEqual(name.strip(), datas[0]['name'].encode('UTF-8'))
                    self.assertEqual(uid, datas[0]['uid'])
                else:
                    # 查询教师班级列表
                    url_grouplist = address + '/api/v1/account/teacher/group'
                    request = urllib2.Request(url_grouplist)
                    content = opener.open(request)
                    response_json_data = json.loads(content.read())
                    datas = response_json_data['data']
                    self.assertEqual(1, len(datas))
                    self.assertEqual(temp_name, datas[0]['name'].encode('UTF-8'))
                    self.assertEqual(uid, datas[0]['uid'])

        except Exception, e:
            logger.error(e.message)
            self.fail()

    #缺少name字段  返回正常,但不修改名称
    def testEditMissName(self):
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

            # 编辑班级,修改名称时 缺少name字段
            url = address + '/api/v1/account/group/edit'
            body = {'group_uid': uid}
            data = json.dumps(body)
            headers = {'Content-Type': 'application/json'}
            request = urllib2.Request(url, data, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(None, response_json_data['message'])
            self.assertEqual(None, response_json_data['data'])

            # 查询教师班级列表,名称没有修改
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            datas = response_json_data['data']
            self.assertEqual(1, len(datas))
            self.assertEqual(name, datas[0]['name'].encode('UTF-8'))
            self.assertEqual(uid, datas[0]['uid'])
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #编辑的时候  uid有误
    # TODO code应该为1
    def testEditWrongUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

            # 编辑班级,修改名称
            url = address + '/api/v1/account/group/edit'
            name = '我的第一个班级改名了' + str(time.time())
            body = {'name': name, 'group_uid': 'wrongUid'}
            data = urllib.urlencode(body)
            request = urllib2.Request(url, data)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])
            self.assertEqual(None, response_json_data['data'])

        except Exception, e:
            logger.error(e.message)
            self.fail()

    #多个班级随机顺序  改名
    def testEditManyClasses(self):
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

            # 随机顺序编辑班级 ,修改名称
            random.shuffle(uids)
            for uid in uids:
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

            # 查询教师班级列表
            url_grouplist = address + '/api/v1/account/teacher/group'
            request = urllib2.Request(url_grouplist)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            datas = response_json_data['data']
            self.assertEqual(len(uids), len(datas))
            for i in range(len(uids)):
                self.assertTrue('改名了' in datas[int(i)]['name'].encode('UTF-8'))
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #多个班级随机顺序  改名为同一个名字
    def testEditManyClasses(self):
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

            # 随机顺序编辑班级 ,修改名称
            random.shuffle(uids)
            for uid in uids:
                url = address + '/api/v1/account/group/edit'
                name = '一起改名啊'
                body = {'name': name, 'group_uid': uid}
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
            self.assertEqual(len(uids), len(datas))
            for i in range(len(uids)):
                self.assertTrue('一起改名啊' in datas[int(i)]['name'].encode('UTF-8'))
        except Exception, e:
            logger.error(e.message)
            self.fail()
