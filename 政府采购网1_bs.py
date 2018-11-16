#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  政府采购网_bs.py
#  Copyright 2018 lyo <lyo@DESKTOP-IG5SQME>

from bs4 import BeautifulSoup
import requests
import time
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

def get_links(url):  # 定义获取详细页url的函数
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #body > div.middle_box > div.middle > div.bargain_box > table > tbody > tr:nth-child(2) > td:nth-child(2) > a
    titlelists = soup.select(
        'body > div.middle_box > div.middle > div.bargain_box > table > tr > td:nth-of-type(2) > a')
    links = soup.select(
        'body > div.middle_box > div.middle > div.bargain_box > table > tr > td:nth-of-type(9) > a:nth-of-type(2)')  # links为url列表

    for link, titlelist in zip(links, titlelists):
        href = link.get("href")
        title = titlelist.get("title")
        get_info(href, title)  # 循环出的url，依次调用get_info函数

def get_info(url, title):  # 定义获取网页信息的函数
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    comps = soup.select(
        'body > div.middle_box > div.middle > div.supp_list > div > table > tr:nth-of-type(2) > td:nth-of-type(2)')
    mans = soup.select(
        'body > div.middle_box > div.middle > div.supp_list > div > table > tr:nth-of-type(2) > td:nth-of-type(4)')
    phones = soup.select(
        'body > div.middle_box > div.middle > div.supp_list > div > table > tr:nth-of-type(3) > td:nth-of-type(2)')
    for comp, man, phone in zip(comps, mans, phones):
        data = {
            'goods': title,
            'unit': comp.get_text().strip(),
            'man': man.get_text().strip(),
            'phone': phone.get_text()
        }
        print(data)  # 获取信息并通过字典的信息打印

if __name__ == '__main__':  # 主入口
    urls = ['http://cgmc.hzft.gov.cn/gpmall/index/moreorders.html?auditstatus=2&pageno={}'.format(str(i)) for i in
            range(1, 100)]  # 构造多页url
    for single_url in urls:
        get_links(single_url)  # 循环调用get_links函数
        time.sleep(2)  # 睡眠2秒
