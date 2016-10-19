#encoding:utf-8
import cookielib
import json
import logging
import random
import unittest
import sys
import urllib
import urllib2

from utils.commonMethod import clearCleasses, loginAndCreateClass

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}


# TODO 上述bug修复后,添加此用例:  学号不重复不一定在一个班内，一个老师教的学生都不应该重复，测试的时候得注意
# TODO 批量创建的学生和之前单个创建的学号重复

class StudentCreateBatch(unittest.TestCase):

    def setUp(self):
        clearCleasses()

    # 批量创建学生
    def testCreateAsList(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid, 'students': [{'name': '张三', 'number': '001'}, {'name': '张四', 'number': '199'}, {'name': '张五', 'number': '001'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(1, len(response_json_data['data']))
            self.assertEqual('001', response_json_data['data'][0]['number'])
            self.assertEqual('张五', response_json_data['data'][0]['name'].encode('UTF-8'))

        except Exception, e:
            logger.error(e.message)
            self.fail()

    #批量创建学号和之前批量创建的学号重复
    def testCreateSameNumber(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            group_uid = loginAndCreateClass(opener)

            # 班级中创建学生
            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid,
                    'students': [{'name': '张三', 'number': '001'}, {'name': '张四', 'number': '199'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(0, len(response_json_data['data']))


            url = address + '/api/v1/account/student/batch'
            data = {'group_uid': group_uid,
                    'students': [{'name': '赵柳', 'number': '008'},
                                 {'name': '赵柳', 'number': '009'},
                                 {'name': '嫦娥', 'number': '009'},
                                 {'name': '李磊', 'number': '001'},
                                 {'name': '李明', 'number': '199'}]}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertEqual(0, response_json_data['code'])
            self.assertEqual(3, len(response_json_data['data']))

        except Exception, e:
            logger.error(e.message)
            self.fail()