#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-16 13:07:57
# @Author  : Yan Chen (cheny.gary@gmail.com)
# @Link    : ${link}
# @Version : $Id$


from urllib import request
import http.cookiejar
import os
import urllib.request
import urllib.parse

# with request.urlopen('file:///Users/garychen/Documents/python%20demo/jiangmeijia2008.html') as webfile:
#     html = webfile.read()
#     htmlcontent =html.decode('GBK')
# html = htmlcontent.encode('utf-8')

# print('Status:', webfile.status, webfile.reason)
# for k, v in webfile.getheaders():
#     print('%s: %s' % (k, v))
# print('Data:', html.decode('utf-8'))


def getHtml(url, daili='', postdata={}):
    """
抓取网页：支持cookie
第一个参数为网址，第二个为POST的数据
"""
    # COOKIE文件保存路径
    filename = 'cookie.txt'

    # 声明一个MozillaCookieJar对象实例保存在文件中
    cj = http.cookiejar.MozillaCookieJar(filename)
    # cj =http.cookiejar.LWPCookieJar(filename)

    # 从文件中读取cookie内容到变量
    # ignore_discard的意思是即使cookies将被丢弃也将它保存下来
    # ignore_expires的意思是如果在该文件中 cookies已经存在，则覆盖原文件写
    # 如果存在，则读取主要COOKIE
    if os.path.exists(filename):

        cj.load(filename, ignore_discard=True, ignore_expires=True)
    # 读取其他COOKIE
    if os.path.exists('subcookie.txt'):
        cookie = open('subcookie.txt', 'r').read()
    else:
        cookie = 'bbb'    # 建造带有COOKIE处理器的打开专家
    proxy_support = urllib.request.ProxyHandler({'http': 'http://' + daili})
    # 开启代理支持
    if daili:
        print('代理:' + daili + '启动')
        opener = urllib.request.build_opener(
            proxy_support, urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler)
    else:
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj))

    # 打开专家加头部
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'),
                         ('Cookie', cookie),
                         ('method', 'GET'),
                         ('scheme', 'https'),
                         ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                         ]

    # 分配专家
    urllib.request.install_opener(opener)
    # 有数据需要POST
    if postdata:
        # 数据URL编码
        postdata = urllib.parse.urlencode(postdata)

        # 抓取网页
        html_bytes = urllib.request.urlopen(url, postdata.encode()).read()
    else:
        html_bytes = urllib.request.urlopen(url).read()

    # 保存COOKIE到文件中
    cj.save(ignore_discard=True, ignore_expires=True)
    return html_bytes
