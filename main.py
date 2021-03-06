#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests #做web请求的库
from bs4 import BeautifulSoup #处理html的库
import itchat
import datetime
from selenium import webdriver
from pyvirtualdisplay import Display
import time
# import argparse
#import threading #多线程库
# import sys

# #表单的url
# formurl = 'https://billing.virmach.com/clientarea.php?action=services'
# #处理登录请求的url
# loginurl = 'https://billing.virmach.com/dologin.php'
#请求包头
header = {
		'authority': 'billing.virmach.com',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.',
		'cache-control':'max-age=0',
		'upgrade-insecure-requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/72.0.3626.119 Chrome/72.0.3626.119 Safari/537.36',
    # 'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'scheme': 'https',
    'Connection': 'keep-alive',
}


#代理，可用可不用，方便burpsuite抓包分析的
proxies = {
    'http': 'https://112.231.80.198:8123'
}

cookies = {'__cfduid=d7df4a06a70ca5fd874d5fac86c9b93ba1549957398; _ga=GA1.2.1857082821.1549957407; _fbp=fb.1.1549957410223.109094711; __mmapiwsid=ba0690f9-331d-406c-b737-1971aaccf757:6e09e41b3e3b63cb0ad25571b298811009b1fe92; __stripe_mid=fcf1b080-08b9-4585-9d5b-5c1d9fdf4eee; WHMCSeXMvUTd4giP5=tnmbdnqg1uk9hvdg7epacofa54; _gid=GA1.2.1519600148.1552028986; _gat=1; crisp-client%2Fsession%2Fb7400af9-fa17-4b41-9910-dbdc0f3ad1f7=session_19a49e3c-960b-40f4-b61a-34f2d421394d'}
#获取token的函数
def gettoken(page):
    #将传进来的html页面传给BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')
    # print(soup.prettify())
    #从页面中找出所有的表单输入
    token = soup.find_all("input")
    #返回的数组有三个元素，而由表单结构可知，第三个输入是我们要获取的token，所以取数组下标为2的元素
    #print(token)
    token = str(token[2])
    #找右边的地一个引号，因为从表单结构可知，token是被双引号包裹的，又知道md5值长度是32，再根据数组”包左不包右“的性质，容易得出token值的范围
    r = token.rfind('"')
    l = r - 32
    token = token[l:r]
    return token

#尝试登录的函数
def login(username, password,loginurl,formurl):
    #token机制是基于session的，session是基于cookies的，所以一定要开启requests的session功能
    res = requests.session()
    #取得页面
    page = res.get(formurl, headers=header, proxies = proxies)
    #获取token
    token = gettoken(page.text)
    #构造post的数据
    data = {'username': username, 'password': password, 'token': token}
    #使用同一个requests对象，在同一个session里进行登录
    #使用代理
    #result = res.post(loginurl, data=data, proxies=proxies)
    #不使用代理
    result = res.post(loginurl, data=data)
    # return(result.text)
    #打印出登录结果， 以及页面长度，基于长度判断的话比较好筛选结果
    return(result.text)

def chkvps(usr,pas):
    # #表单的url
    formurl = 'https://billing.virmach.com/clientarea.php?action=services'
    # #处理登录请求的url
    loginurl = 'https://billing.virmach.com/dologin.php'
    clstapg = login(usr,pas,loginurl,formurl)
    # print(clstapg)
    soup = BeautifulSoup(clstapg, 'html.parser')
    sta = soup.find_all('span')
    sta = str(sta[-3].string)
    return(sta)

def getlogin(file):
	try :
		dict =[]
		f = open(file)
		for w in f.readlines():
			dict.append(w)
		return(dict)
	except:
		print('Can\'t find the file')

if __name__ == '__main__':
			# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/72.0.3626.119 Chrome/72.0.3626.119 Safari/537.36'
			# chrome_opt = webdriver.ChromeOptions()
			# chrome_opt.add_argument('--headless')
			# chrome_opt.add_argument('--disable-gpu')
			# chrome_opt.add_argument('--no-sandbox')
			# chrome_opt.add_argument('--disable-dev-shm-usage')
			# chrome_opt.add_argument('user-agent={user_agent}')
			# driver = webdriver.Chrome(chrome_options=chrome_opt,executable_path='/usr/pythoncode/cheser/chromedriver') #注意需要将chromedriver放入代码中方可运行
			# URL = 'https://billing.virmach.com/clientarea.php?action=services'
			# driver.get(URL)
			# time.sleep(10) # 要大于5s
			# html=driver.page_source # 获取实际页面的html
			# print(html)
			# driver.quit()

	    #取得页面

	    # print(page)

	logininfo = getlogin('loginfile')
	uname = logininfo[0]
	pword = logininfo[1]
	scheduled_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	flag=0
	while True:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		if now == scheduled_time and flag==0:
			# itchat.auto_login(hotReload=True, enableCmdQR=2)
			sersta = chkvps(uname,pword)
			# itchat.send_msg('%s Virmach server now is on %s'%(now, sersta),)
			print('%s Virmach server now is on %s'%(now, sersta))
			flag=1
		else:
			if flag==1:
				scheduled_time=(datetime.datetime.now()+datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
				flag=0

#获取密码字典的文件对象
# def getdict(file):
#     dict = []
#     try:
#         f = open(file, "r")
#         for p in f.readlines():
#             dict.append(p)

#         return dict
#     except:
#         print('文件异常')

#获取命令行参数
#爆破的用户名
#username = sys.argv[1]
#密码字典的文件名
#passfile = sys.argv[2]

# t=args.thread
# tpool=[]
#file = getdict(passfile)
#遍历字典
# for p in file:
#     #将取出的结果转换成字符串
#     p = str(p)
#     #去掉特殊符号
#     p = p.strip().strip('\n').strip('\r')
#     #多线程破解
#     t = threading.Thread(target=login, args=(username, p))
#     # tpool.append(tt)
#     t.start()
#     # 用了join会稍微慢点，但是安全，和不用多线程速度差不多，如此join多线程的意义不大。
#     t.join()