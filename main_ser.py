#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import json
import datetime

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
	nowm = datetime.datetime.now().strftime("%Y-%m")
	gamelist = cherocket(nowm)
	for game in gamelist:
		stardate = game['startTime'][:10]
		nowd = datetime.datetime.now().strftime("%Y-%m-%d")
		print(stardate+nowd)
		# if stardate == nowd.text:
		# 	print('今日有比赛')
		# else:
		# 	print('今日无比赛')
