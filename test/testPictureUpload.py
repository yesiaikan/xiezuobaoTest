#encoding:utf-8
import cookielib
import json
import logging
import unittest
import sys
import urllib2
import uuid

import requests
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from utils.commonMethod import clearCleasses, loginAndCreateClass, my_Login, createExam, clearExams

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}


class PictureUpload(unittest.TestCase):

    def setUp(self):
        clearCleasses()
        clearExams()

    # 上传图片
    def testPicture(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            url = address + '/api/v1/pool/image/access?exercise_uid=' + exam_uid
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)

            accessid = response_json_data['data']['accessid']
            url = response_json_data['data']['host']
            expire = response_json_data['data']['expire']
            signature = response_json_data['data']['signature']
            policy = response_json_data['data']['policy']
            dir = response_json_data['data']['dir']

            # register_openers()
            # data = {'name': str(filename), 'key': str(dir) + filename, 'policy': str(policy),
            #         'signature': str(signature), 'OSSAccessKeyId': str(accessid), 'file': open('test.jpg', 'rb')}
            # datagen, headers = multipart_encode(data)
            # request = urllib2.Request(url, datagen, headers)
            # content1 = urllib2.urlopen(request)
            # response_json_data = json.loads(content1.read())
            # self.assertEqual(200, content.code)

            filename = uuid.uuid4().hex + '-origin.jpg'
            data = {'name': str(filename), 'key': str(dir) + filename, 'policy': str(policy),
                    'signature': str(signature), 'OSSAccessKeyId': str(accessid)}
            files = {'file': open('test.jpg', 'rb')}
            resp = requests.post(url, data=data, files=files)
            self.assertEqual(204, resp.status_code)

        except Exception, e:
            logger.error(e.message)
            self.fail()


    # 获取签名缺少参数 TODO  不带参数不应响应code,不应返回签名信息
    def testPictureMissExamUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            url = address + '/api/v1/pool/image/access'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertFalse(0 == response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()


    #参数错误 TODO 使用错误的exercise_uid 不应该返回签名信息,code不应该为0
    def testPictureWrongExamUid(self):
        try:
            cookieJar = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
            exam_uid, group_uid = createExam(opener)

            url = address + '/api/v1/pool/image/access?exercise_uid=' + 'wrong'
            request = urllib2.Request(url)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
            self.assertEqual(200, content.code)
            self.assertFalse(0 == response_json_data['code'])
        except Exception, e:
            logger.error(e.message)
            self.fail()