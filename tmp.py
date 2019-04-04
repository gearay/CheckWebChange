#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-03 21:43:49
# @Author  : gearay (cheny.gary@gmail.com)
# @Link    : http://example.org
# @Version : $Id$

# 访问https://www.rememberthemilk.com/json/gearay/ 取得rtm信息
import requests
import json
import datetime



def getrtm(uname, pword):
	rtmpost = {"username": uname, "password":pword, "remember":"on"}
	urlpath = "https://www.rememberthemilk.com/json/"+uname
	authurl = "https://www.rememberthemilk.com/auth.rtm"
	res = requests.session()
	authpage = res.post(authurl, data= rtmpost)
	contentpage = res.get(urlpath)
	return(contentpage.text)

    
# 取出当日日程
def getrtmTask(jsonp):
	# tasks = json.loads(jsonp)
	curt = (datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d" ),("%Y-%m-%d"))).timestamp()
	jsoncts = (json.loads(jsonp))['tasks']
	taskContl = []
	for task in jsoncts:
		if task['date_due_has_time']  and  task['date_due'] > (curt-86400)*1000 and task['date_due'] <curt*1000:
			taskContl.append((datetime.datetime.fromtimestamp(task['date_due']/1000)).strftime("%H:%M") + task['name'])
	return(taskContl)

def getlogin(file):
	try :
		dict =[]
		f = open(file)
		for w in f.readlines():
			dict.append(w.split("/"))
		return(dict)
	except:
		print('Can\'t find the file')

if __name__ == '__main__':
	loginfo = getlogin('loginfile')
	un =  [x[1]  for x in loginfo if x[0] == 'rtm'][0]
	pa =  [x[2]  for x in loginfo if x[0] == 'rtm'][0]	
	pagej = getrtm(un,pa)
	msgl = getrtmTask(pagej)
	msg = (' ').join(msgl)
	print(msg)

