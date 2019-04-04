#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import json
import datetime
import itchat
import time


header = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.',
		'cache-control':'max-age=0',
		'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'scheme': 'https',
    'Connection': 'keep-alive',
}

proxies = {
    'http': 'https://112.231.80.198:8123'
}

def cherocket():
	se = requests.session()
	page = se.get('https://mat1.gtimg.com/apps/hpage2/nbateammatchlist_10.json', headers =header)
	page = re.findall(re.compile(r'[(](.*)[)]', re.S),page.text) 
	jsonp = json.loads(page[0])
	gamelist = jsonp[datetime.datetime.now().strftime("%Y-%m")]
	gflag = 0
	nowd = datetime.datetime.now().strftime("%Y-%m-%d")
	for game in gamelist:
		
		if game['startTime'][:10] == nowd:
			return('今日有比赛，%s %s 对 %s' % (game['startTime'][-8:],game['leftName'],game['rightName']))
			gflag = 1

	if gflag == 0:
		return('今日无火箭比赛')


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
		if task['date_due_has_time']  and  task['date_due'] > (curt)*1000 and task['date_due'] <(curt+86400)*1000:
			taskContl.append((datetime.datetime.fromtimestamp(task['date_due']/1000)).strftime("%H:%M") + task['name'])
	if len(taskContl):
		return(" ".join(taskContl))
	else:
		return("今日无任务")

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

	flag=0
	scheduled_time = '2019-04-04 5:00'
	# scheduled_time = now.strftime("%Y-%m-%d %H:%M")
	while True:
		if datetime.datetime.now() >= datetime.datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M") and flag==0:
			itchat.auto_login(hotReload=True, enableCmdQR=2)
			#查看当日火箭比赛信息
			# try:
			# 	msgrocket = cherocket()
			# except Exception as e:
			# 	msgrocket = "比赛信息查询有误"
			#查看当日rtm任务
			try:
				loginfo = getlogin('loginfile')
				un =  [x[1]  for x in loginfo if x[0] == 'rtm'][0]
				pa =  [x[2]  for x in loginfo if x[0] == 'rtm'][0]
				pagertm = getrtm(un.strip(),pa。strip())
				msgrtm = getrtmTask(pagertm)
			except Exception as e:
				msgrtm = "rtm任务查询有误"
			# itchat.send_msg(msgrocket)
			itchat.send_msg(msgrtm)
			flag = 1
		else:
			if flag==1:
				scheduled_time=(datetime.datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M")+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
				print(scheduled_time)
				flag=0



