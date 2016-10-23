#encoding:utf-8
import cookielib
import json
import logging
import random
import unittest
import sys
import urllib
import urllib2

from utils.commonMethod import clearCleasses, loginAndCreateClass, clearExams

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}

class ExaminationCreate(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    def testCreateAll(self):
        try:
            # subject 为 chinese,math,english,physics,chemistry,biology,history,geography,phlitics,others
            subjects = ['politics', 'chinese', 'math', 'english', 'physics', 'chemistry', 'biology', 'history', 'geography', 'others']
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            loginAndCreateClass(opener)

            # 创建考试
            for subject in subjects:
                url = address + '/api/v1/exercise/edit'
                name = '考试 ' + subject + ' 啦'
                # subject = subjects[1]
                data = {'name': name, 'subject': subject, 'manual': True}
                postData = json.dumps(data)
                request = urllib2.Request(url, postData, headers)
                content = opener.open(request)
                response_json_data = json.loads(content.read())
                self.assertEqual(200, content.code)
                self.assertEqual(0, response_json_data['code'])
                self.assertEqual(name, response_json_data['data']['name'].encode('UTF-8'))
                # self.assertEqual(subject, response_json_data['data']['subject'])
                exam_uid = response_json_data['data']['uid']
                self.assertIsNotNone(exam_uid)

        #     TODO 校验列表
        except Exception, e:
            logger.error(e.message)
            self.fail()

