# -*- coding: utf-8 -*-

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

import requests as REQ
from bs4 import BeautifulSoup as BS

Year = 1071

Urls = {
    'index': 'http://selcrs.nsysu.edu.tw/',
    'menu4': 'http://selcrs.nsysu.edu.tw/menu4/',
    'check': 'http://selcrs.nsysu.edu.tw/menu4/Studcheck.asp',
    'valid': 'http://selcrs.nsysu.edu.tw/validcode.asp',
    'selected': 'http://selcrs.nsysu.edu.tw/menu4/query/slt_result.asp',
    'search': 'http://selcrs.nsysu.edu.tw/menu1/dplycourse.asp',
    'menu': 'http://selcrs.nsysu.edu.tw/menu4/Studfun.asp',
    'step2': 'http://selcrs.nsysu.edu.tw/menu4/addcourse/ssprs.asp'
}

Encoding = 'big5'

Proxies = {
    'http': 'https://208.97.119.150:55509',
    'https': 'https://208.97.119.150:55509'
}

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

def CheckUrl(url_key):
    return Urls[url_key] if url_key in Urls else url_key

def Session():
    return REQ.Session()

def SessGetBS(sess, url_key, params = None, headers = Headers, stream = False):
    return BS(SessGet(sess, url_key, params).text, 'html.parser')

def SessPostBS(sess, url_key, data = None, headers = Headers, stream = False):
    return BS(SessPost(sess, url_key, data).text, 'html.parser')

def SessGet(sess, url_key, params = None, headers = Headers, stream = False):
    req = sess.get(CheckUrl(url_key), headers = headers, params = params, stream = stream, timeout = 10)
    req.encoding = Encoding
    return req

def SessPost(sess, url_key, data = None, headers = Headers, stream = False):
    req = sess.post(CheckUrl(url_key), headers = headers, data = data, stream = stream, timeout = 10)
    req.encoding = Encoding
    return req

def Get(url_key, params = None, headers = Headers):
    req = REQ.get(CheckUrl(url_key), headers = headers, params = params, timeout = 10)
    req.encoding = Encoding
    return req.text

def Post(url_key, data = None, headers = Headers):
    req = REQ.post(CheckUrl(url_key), headers = headers, data = data, timeout = 10)
    req.encoding = Encoding
    return req.text