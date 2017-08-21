#coding:utf-8

import urllib2
import traceback
from bs4 import BeautifulSoup
import time
import requests
import random
import os,sys

#翻页的后缀
page_down_up_houzui="?start=%s&type=T"
common_inner_url = "https://book.douban.com/tag/%s"
page_down_up_url = "https://book.douban.com/tag/%s%s"
down_load_depth = 10

def getCurrentTime():
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

def randHeader():
    '''
    随机生成User-Agent
    :return:
    '''
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/ 5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                       'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0'
                       ]
    result = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return result

def download(url,header="rand",tries_num=5,sleep_time=0,time_out=10,max_retry=5,isproxy=False):
	sleep_time_p = sleep_time
	time_out_p = time_out
	tries_num_p = tries_num
	if header == 'rand':
		header = randHeader()
	try:
		res = requests.session()
		if isproxy == 1:
			res = requests.get(url, headers=header, timeout=time_out, proxies=proxy)
		else:
			res = requests.get(url, headers=header, timeout=time_out_p)
		res.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
	except: 
		sleep_time_p = sleep_time_p + 10
		time_out_p = time_out_p + 10
		tries_num_p = tries_num_p - 1
		# 设置重试次数，最大timeout 时间和 最长休眠时间
		if tries_num_p > 0:
			time.sleep(sleep_time_p)
			print (getCurrentTime(), url, 'url connection error: 第', max_retry - tries_num_p, u'次 retry connection')
			return download(url, tries_num=tries_num_p, sleep_time=sleep_time_p, time_out=time_out_p,max_retry=max_retry)
	return res
	

def down_load_type(type_dict):
	url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-hot"
	html = download(url).text
	if html:
		soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
		content = soup.find("div",class_="grid-16-8 clearfix")
		tmp = content.div.find_all("div")
		labels = tmp[1].find_all("div")
		for label in labels:
			lines = label.table.find_all("tr")
			for line in lines:
				heng = line.find_all("td")
				for item in heng:
					key = item.a.string.encode("utf-8")
					value =  int(item.b.string.encode("utf-8").lstrip("(").rstrip(")"))
					type_dict[key] =value
	return 0


def md5_bookname(bookname):
	import hashlib
	return hashlib.md5(bookname).hexdigest()

def extrace_digit_from_string(s):
	import re
	_d = re.findall(r"\d+",s)
	return _d

#load crawed urls
def load_crawed_except_urls():
	crawed_urls = set()
	except_urls = set()
	with open("./crawed_urls") as fin:
		for line in fin:
			url = line.rstrip("\n").split("\t")[0]
			crawed_urls.add(url)
	with open("./except_url") as fin:
		for line in fin:
			url = line.rstrip("\n").split("\t")[0]
			except_urls.add(url)
	return crawed_urls,except_urls


def parse_page_url(url_set):
	pair_extract_url_con = set()
	#load crawed urls
	crawed_urls,except_urls = load_crawed_except_urls()
	url_set = (url_set - crawed_urls) | except_urls
	fexcept = open("./except_url","w")
	with open("./bookinfo.txt","a") as fout:
		for url in url_set:
			if url in crawed_urls:
				sys.stderr.write("the url:%s is already crawed\n" % url)
				continue
			html = download(url).text
			print url
			if html:
				soup = BeautifulSoup(html,"html.parser",from_encoding='utf-8')
				content = soup.find_all("li",class_="subject-item")
				for item in content:
					_tmp = item.find("div",class_="info")
					book_name = _tmp.h2.a["title"].encode("utf-8")
					bookid = md5_bookname(book_name)
					book_url = _tmp.h2.a["href"].encode("utf-8")
					pair_extract_url_con.add(book_url)
					_tmp_span =  _tmp.find("div",class_="star clearfix").find_all("span")
					try:
						score = _tmp_span[1].string.encode("utf-8")
					except:
						fexcept.write(url+"\n")
						sys.stderr.write("invalid score error: %s\n" % url)
						continue
					book_people = extrace_digit_from_string(_tmp_span[2].string.strip("\n").strip(" "))[0].encode("utf-8")
					fout.write("%s\t%s\t%s\t%s\t%s\n" % (bookid,book_name,book_url,score,book_people))
                    #write file at once
					fout.flush()
					sleep_time = random.randint(5,10)
					time.sleep(sleep_time)
					parse_pair_url(book_name,book_url)
			with open("./crawed_urls","a") as fcraw:
				fcraw.write(url+"\n")
				fcraw.flush()
			sleep_time = random.randint(3,5)
			time.sleep(sleep_time)	

def parse_pair_url(book_name,url):
	pair_set = set()
	with open("book_pair.txt","a") as fout:
		html = download(url).text
		if html:
			soup = BeautifulSoup(html,"html.parser",from_encoding="utf-8")
			content = soup.find_all("div",class_="content clearfix")
			for i in range(len(content)):
				_tmp = content[i].find_all("dl")
				for book in _tmp:
					try:
						if len(content) == 1:
							alike_book = book.dd.a.get_text().strip("\n").strip(" ").encode("utf-8")[:-1]
						else:
							if i == 1:
								alike_book = book.dd.a.get_text().strip("\n").strip(" ").encode("utf-8")[:-1]
							else:
								alike_book = book.dd.a.get_text().strip("\n").strip(" ").encode("utf-8")
					except AttributeError as e:
						continue
					pair_set.add(alike_book)
		fout.write("%s\t%s\n" % (book_name,"\t".join(pair_set)))			
		fout.flush()

#直接产生数据
def down_load_page_url():
	url_set = set()
	type_dict = {}
	down_load_type(type_dict)
	for item in type_dict.keys():
		for i in range(down_load_depth):
			if i == 1:
				url = common_inner_url % (item)
			else:
				tmp = page_down_up_houzui % (20*(i-1))
				url = page_down_up_url % (item,tmp)
			url_set.add(url)			
	parse_page_url(url_set)		
	return 0
	

if __name__ == "__main__":
#	type_dict = {}
#	down_load_type(type_dict)
#	print len(type_dict)
#debug
#	for k,v in type_dict.iteritems():
#		print "{0}\t{1}".format(k,v)
	down_load_page_url()
	#randHeader()
