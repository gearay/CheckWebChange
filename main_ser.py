#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import json
import datetime
import itchat

header = {
		'authority': 'billing.virmach.com',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.',
		'cache-control':'max-age=0',
		'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'scheme': 'https',
    'Connection': 'keep-alive',
}

def cherocket(date):
	se = requests.session()
	page = se.get('https://mat1.gtimg.com/apps/hpage2/nbateammatchlist_10.json', headers =header)
	page = re.findall(re.compile(r'[(](.*)[)]', re.S),page.text) 
	jsonp = json.loads(page[0])
	games = jsonp[date]
	return(games)




if __name__ == '__main__':
	now = datetime.datetime.now()
	# now = datetime.datetime.now()+datetime.timedelta(days=1)
	gamelist = cherocket(now.strftime("%Y-%m"))
	flag=0
	scheduled_time = '2019-03-09 07:00'
	while True:
		if now.strftime("%Y-%m-%d %H:%M") == scheduled_time and flag==0:
			itchat.auto_login(hotReload=True, enableCmdQR=2)
			gflag = 0
			nowd = now.strftime("%Y-%m-%d")		
			for game in gamelist:
				
				if game['startTime'][:10] == nowd:
					itchat.send_msg('今日有比赛，%s %s 对 %s' % (game['startTime'][-8:],game['leftName'],game['rightName']))
					gflag = 1

			if gflag == 0:
				itchat.send_msg('今日无火箭比赛')
			flag = 1
		else:
			if flag==1:
				scheduled_time=(now+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
				flag=0


