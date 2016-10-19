#encoding:utf-8

import cookielib
import json
import logging
import urllib
import urllib2

import sys

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))
address = 'http://pigai.hexinedu.com'

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
