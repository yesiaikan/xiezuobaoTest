# #encoding:utf-8
# import cookielib
# import json
# import logging
# import random
# import unittest
# import sys
# import urllib
# import urllib2
#
# from utils.commonMethod import clearCleasses, loginAndCreateClass
#
# logger = logging.getLogger()
# logger.level = logging.DEBUG
# logger.addHandler(logging.StreamHandler(sys.stdout))
#
# address = 'http://pigai.hexinedu.com'
# headers = {'Content-Type': 'application/json'}
#
# # TODO 创建班级时name字段值测试
# # TODO 创建班级时group_uid字段值测试
# # TODO 创建班级时number字段测试,包括非数字等其他字符
# # TODO 缺少name 或者 group_uid 或者 number字段
#
# # TODO 多次创建学生名称相同,是否创建成功
# # TODO 多次创建学生 number 相同,是否创建成功
#
# class StudentCreate(unittest.TestCase):
#
#     def setUp(self):
#         clearCleasses()
#
#     # 班级中创建学生
#     def testCreate(self):
#         try:
#             cookieJar = cookielib.CookieJar()
#             opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
#             group_uid = loginAndCreateClass(opener)
#
#             # 班级中创建学生
#             url = address + '/api/v1/account/student/edit'
#             data = {'name': '张三', 'number': '001', 'group_uid': group_uid}
#             postData = json.dumps(data)
#             request = urllib2.Request(url, postData, headers)
#             content = opener.open(request)
#             response_json_data = json.loads(content.read())
#             self.assertEqual(200, content.code)
#             self.assertEqual(0, response_json_data['code'])
#             self.assertEqual('张三', response_json_data['data']['name'].encode('UTF-8'))
#             self.assertEqual('student', response_json_data['data']['role'])
#             stu_uid = response_json_data['data']['uid']
#             self.assertIsNotNone(stu_uid)
#
#             # 查询班级中学生列表
#             url = address + '/api/v1/account/student/list?group_uid=' + group_uid
#             request = urllib2.Request(url)
#             content = opener.open(request)
#             response_json_data = json.loads(content.read())
#             self.assertEqual(200, content.code)
#             self.assertEqual(0, response_json_data['code'])
#             self.assertEqual(1, len(response_json_data['data']))
#             self.assertEqual('张三', response_json_data['data'][0]['name'].encode('UTF-8'))
#             self.assertEqual('001', response_json_data['data'][0]['number'])
#             self.assertEqual(stu_uid, response_json_data['data'][0]['uid'])
#         except Exception, e:
#             logger.error(e.message)
#             self.fail()
#
#     # 创建学生姓名为空
#     def testCreateNoneName(self):
#         try:
#             cookieJar = cookielib.CookieJar()
#             opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
#             group_uid = loginAndCreateClass(opener)
#
#             # 班级中创建学生
#             i = 0
#             names = [None, '  ', '']
#             for name in names:
#                 i += 1
#                 url = address + '/api/v1/account/student/edit'
#                 data = {'name': name, 'number': str(i), 'group_uid': group_uid}
#                 postData = json.dumps(data)
#                 request = urllib2.Request(url, postData, headers)
#                 content = opener.open(request)
#                 response_json_data = json.loads(content.read())
#                 self.assertEqual(200, content.code)
#                 self.assertEqual(1, response_json_data['code'])
#
#         except Exception, e:
#             logger.error(e.message)
#             self.fail()
#
#
#     # 创建学生number为空 TODO
#     def testCreateNoneName(self):
#         try:
#             cookieJar = cookielib.CookieJar()
#             opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
#             group_uid = loginAndCreateClass(opener)
#
#             # 班级中创建学生
#             i = 0
#             numbers = [None, '', ' ']
#             for number in numbers:
#                 i += 1
#                 url = address + '/api/v1/account/student/edit'
#                 data = {'name': '张柳', 'number': number, 'group_uid': group_uid}
#                 postData = json.dumps(data)
#                 request = urllib2.Request(url, postData, headers)
#                 content = opener.open(request)
#                 response_json_data = json.loads(content.read())
#                 self.assertEqual(200, content.code)
#                 self.assertEqual(1, response_json_data['code'])
#
#         except Exception, e:
#             logger.error(e.message)
#             self.fail()