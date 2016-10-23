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

import datetime

from utils.commonMethod import clearCleasses, loginAndCreateClass

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}

class StudentCreateBatch(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 批量创建学生
    def testCreateAsList(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生, 学号有重复
            number = str(time.time()).split('.')[0] + str(datetime.datetime.now().microsecond)
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid, 'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number}, {'name': '张五', 'number': number+'1'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual(number, response_json_data['data'][0]['number'])
            self.assertEqual('张四', response_json_data['data'][0]['name'].encode('UTF-8'))

            #查询班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(2, len(response_json_data['data']))
        except Exception, e:
            logger.error(e.message)
            self.fail()

    #批量创建学号和之前批量创建的学号重复
    # TODO 存在bug  number和之前列表重复 仍会创建成功
    def testCreateSameNumber(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + str(datetime.datetime.now().microsecond)
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))


            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid,
                    'students': [{'name': '赵柳', 'number': number},  #和之前重复
                                 {'name': '赵柳', 'number': number+2},
                                 {'name': '嫦娥', 'number': number+3},
                                 {'name': '李磊', 'number': number+4}, #自身重复
                                 {'name': '李明', 'number': number+4}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(2, len(response_json_data['data']))

            # 查询班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(5, len(response_json_data['data']))

        except Exception, e:
            logger.error(e.message)
            self.fail()


    # 批量创建学号和其他班级的学号重复
    # TODO  有bug  班级之间学号重复不应该创建成功
    def testCreateSameNumber1(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + str(datetime.datetime.now().microsecond)
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))


            #创建其他班级
            url = address + '/api/v1/account/group/edit'
            name = '我的第二个班级' + str(time.time())
            body = {'name': name}
            data = json.dumps(body)
            request = urllib2.Request(url, data, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            othre_group_uid = response_json_data['data']['uid']

            # 其他班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': othre_group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number + 2}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))

            # 查询第一个班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(2, len(response_json_data['data']))

            # 查询第二个班级列表
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

    # TODO 目前是:同一个班级中删除的学号,又能创建成功;策略来定
    def testCreateDeleteThanCreat(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + str(datetime.datetime.now().microsecond)
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number + '1'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))

            # 查询班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(2, len(response_json_data['data']))
            stu_uid = response_json_data['data'][0]['uid']
            stu_uid1 = response_json_data['data'][1]['uid']

            # 删除学生信息
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': group_uid, 'user_uid': [stu_uid]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            # 查询第一个班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual(stu_uid1, response_json_data['data'][0]['uid'])

            #再创建学号为 number的学生
            url = address + '/api/v1/account/student/batch'
            # number = int(str(time.time()).split('.')[0]) + 10
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))

            # 查询第一个班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(2, len(response_json_data['data']))
        except Exception, e:
            logger.error(e.message)
            self.fail()

    # 其他班级被删除,新建班级中添加删除班级的学生学号
    # TODO 目前不能创建成功
    def testCreateDeleteThanCreat(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + str(datetime.datetime.now().microsecond)
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number+'1'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))

            # 查询班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(2, len(response_json_data['data']))
            stu_uid = response_json_data['data'][0]['uid']
            stu_uid1 = response_json_data['data'][1]['uid']

            #删除班级
            clearCleasses()

            # 创建其他班级
            url = address + '/api/v1/account/group/edit'
            name = '我的第二个班级' + str(time.time())
            body = {'name': name}
            data = json.dumps(body)
            request = urllib2.Request(url, data, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            oter_group_uid = response_json_data['data']['uid']

            # 其他班级中创建学生  number和其他班级的重复
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': oter_group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number+'2'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))


            # 查询第一个班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + oter_group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))

        except Exception, e:
            logger.error(e.message)
            self.fail()


    # 其他班级被删除,删除之前清空学生, 新建班级中添加删除班级的学生学号
    # TODO 目前不能创建成功
    def testCreateDeleteThanCreat1(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            number = str(time.time()).split('.')[0] + str(datetime.datetime.now().microsecond)
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number + '1'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))

            # 查询班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(2, len(response_json_data['data']))
            stu_uid = response_json_data['data'][0]['uid']
            stu_uid1 = response_json_data['data'][1]['uid']

            # 删除学生信息
            url = address + '/api/v1/account/group/student/quit'
            data = {'group_uid': group_uid, 'user_uid': [stu_uid, stu_uid1]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])

            # 查询班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))

            # 删除班级
            clearCleasses()

            # 创建其他班级
            url = address + '/api/v1/account/group/edit'
            name = '我的第二个班级' + str(time.time())
            body = {'name': name}
            data = json.dumps(body)
            request = urllib2.Request(url, data, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            oter_group_uid = response_json_data['data']['uid']

            # 其他班级中创建学生  number和其他班级的重复
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': oter_group_uid,
                    'students': [{'name': '张三', 'number': number}, {'name': '张四', 'number': number + '2'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))

            # 查询第一个班级列表
            url = address + '/api/v1/account/student/list?group_uid=' + oter_group_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))

        except Exception, e:
            logger.error(e.message)
            self.fail()

    #创建学生时,students列表为空
    def testCreateEmptyList(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid, 'students': []}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))

            # 查询班级列表
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


    #创建学生时,students缺失
    def testCreateMissStudents(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])

            # 查询班级列表
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

    # 创建学生时, group_uid有误
    def testCreateEmptyList(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': 'wrong_uid', 'students': []}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])

            # 查询班级列表
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

    # 创建学生时, group_uid缺少
    def testCreateEmptyList(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'students': []}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(1, response_json_data['code'])

            # 查询班级列表
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