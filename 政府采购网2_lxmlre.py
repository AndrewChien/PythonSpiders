#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  政府采购网_lxmlre.py
#  Copyright 2018 lyo <lyo@DESKTOP-IG5SQME>

from lxml import etree
import re
import pymysql
import requests
import time

conn = pymysql.connect(host='localhost', user='root', passwd='123', db='spidertest', port=3306, charset='utf8')
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

def get_links(url):  # 定义获取详细页url的函数
    wb_data = requests.get(url, headers=headers)
    selector = etree.HTML(wb_data.text)
    titlelists = selector.xpath('//td[@align="left"]/a/@title')
    links = selector.xpath('//td[@style="padding-left:4.5em;"]/a[@style="color:red;clear:left;"]/@href')
    for link, titlelist in zip(links, titlelists):
        get_info(link, titlelist)  # 循环出的url，依次调用get_info函数

def get_info(url, title):  # 定义获取网页信息的函数
    wb_data = requests.get(url, headers=headers)
    comps = re.findall('<td rowspan="2" style="text-align:left; padding:0 .75em;">(.*?)</td>',wb_data.text,re.S)[0]
    temp = re.findall('<td height="36">(.*?)</td>',wb_data.text,re.S)
    mans = temp[1]
    phones = temp[3]
    print("商品名称：{0}，采购单位：{1}，采购人：{2}，联系方式：{3}".format(title,comps,mans,phones))

    cursor.execute(
        "insert into govpurchase (title,comps,mans,phones) values(%s,%s,%s,%s)",
        (str(title), str(comps), str(mans), str(phones)))

if __name__ == '__main__':  # 主入口
    urls = ['http://cgmc.hzft.gov.cn/gpmall/index/moreorders.html?auditstatus=2&pageno={}'.format(str(i)) for i in
            range(1, 100)]  # 构造多页url
    time1 = time.time()
    for single_url in urls:
        get_links(single_url)  # 循环调用get_links函数
        time.sleep(1)  # 睡眠2秒
        conn.commit()
    time2 = time.time()
    print(time2 - time1)
