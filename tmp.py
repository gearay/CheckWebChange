#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-03 21:43:49
# @Author  : gearay (cheny.gary@gmail.com)
# @Link    : http://example.org
# @Version : $Id$

# 访问https://www.rememberthemilk.com/json/gearay/ 取得rtm信息
import requests



def getrtm(uname, pword):
	rtmpost = {"username": uname, "password":pword, "remember":"on"}
	urlpath = "https://www.rememberthemilk.com/json/gearay"
	authurl = "https://www.rememberthemilk.com/auth.rtm"
	res = requests.session()
	authpage = res.post(authurl, data= rtmpost)
	contentpage = res.get(urlpath)
	return(contentpage.json())

    
# 取出当日日程

# 发送
if __name__ == '__main__':
