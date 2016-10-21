#encoding:utf-8

import cookielib
import json
import logging
import urllib
import urllib2

import sys

import time

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

address = 'http://pigai.hexinedu.com'
headers = {'Content-Type': 'application/json'}

def clearCleasses():
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


        # 查询班级列表
        url_grouplist = address + '/api/v1/account/teacher/group'
        request = urllib2.Request(url_grouplist)
        content = opener.open(request)
        response_json_data = json.loads(content.read())
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

    except Exception, e:
        logger.error(e.message)


def loginAndCreateClass(opener):
    try:
        username = 'muli'
        password = '123123'
        url = address + '/api/v1/account/login'
        data = {'username': username, 'password': password}
        postData = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url, postData, headers)
        content = opener.open(request)
        response_json_data = json.loads(content.read())


        # 创建班级
        url = address + '/api/v1/account/group/edit'
        name = '我的第一个班级' + str(time.time())
        body = {'name': name}
        data = json.dumps(body)
        request = urllib2.Request(url, data, headers)
        content = opener.open(request)
        response_json_data = json.loads(content.read())
        group_uid = response_json_data['data']['uid']
        return group_uid
    except Exception, e:
        logger.error(e.message)


def clearExams():
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

        # 查看教师考试列表
        url = address + '/api/v1/exercise/list'
        request = urllib2.Request(url)
        content = opener.open(request)
        response_json_data = json.loads(content.read())
        datas = response_json_data['data']
        for data in datas:
            exam_uid = data['uid']
            url = address + '/api/v1/exercise/delete'
            data = {'exercise_uid': exam_uid}
            postData = json.dumps(data)
            request = urllib2.Request(url, postData, headers)
            content = opener.open(request)
            response_json_data = json.loads(content.read())
    except Exception, e:
        logger.error(e.message)