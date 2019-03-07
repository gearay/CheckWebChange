#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

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
	return(page)

def getplay(pagec):
	soup = BeautifulSoup(pagec, 'json.parser')
	return(soup)

if __name__ == '__main__':
	result = getplay(cherocket(37))
	print(result)




