#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  创客小说网.py
#  Copyright 2018 lyo <lyo@DESKTOP-IG5SQME>

from lxml import etree
import requests
import time
import sys

type = sys.getfilesystemencoding()
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
}

domain = 'https://m.ckxsw.com'
f = open('D:/村野桃花朵朵开.txt','a+')

def get_links(url):
    wb_data = requests.get(url, headers = headers)
    selector = etree.HTML(wb_data.text)
    lists = selector.xpath('//div[@class="info_chapters"]/ul[2]/li/a/@href')
    try:
        for list in lists:
            get_info(domain + list)
    except:
        pass

def get_info(list):
    wb_data = requests.get(list, headers = headers)
    html = wb_data.text.encode('iso-8859-1').decode('gbk')
    selector = etree.HTML(html)
    try:
        tt = selector.xpath('//div[@class="nr_function"]/h1/text()')[0]
        ct = selector.xpath('//div[@class="novelcontent"]/text()')
        print("{}\n".format(tt))
        f.write("{}\n".format(tt))
        for c in ct:
            print("{}\n".format(c))
            f.write("{}\n".format(c))
    except:
        pass

if __name__ == '__main__':
    urls = ['https://m.ckxsw.com/0/461_{}/#all'.format(str(i)) for i in range(1, 22)]
    time1 = time.time()
    for single_url in urls:
        get_links(single_url)
        time.sleep(5)
    f.close()
    time2 = time.time()
    print(time2 - time1)
