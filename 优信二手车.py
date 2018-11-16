#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  优信二手车（一成购 + 5万公里内 + 自动挡 + 国五 + 价格递增）.py
#  Copyright 2018 lyo <lyo@DESKTOP-IG5SQME>

from bs4 import BeautifulSoup
import requests
import time
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}
f = open('D:/Projects/python/今日优信数据.txt','a+')

def get_links(url):  # 定义获取详细页url的函数
    wb_data = requests.get(url, headers=headers)
    wb_data.encoding = wb_data.apparent_encoding  # 转换编码，不然中文会显示乱码，也可以r.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    names = soup.select(
        'body > div.car-sale-wrap.sale07 > div.carlist-show > div._list-con.list-con.clearfix.ab_carlist > ul > li.con.caritem.conHeight > div.across > a.aimg > div.pad > h2 > span')
    useds = soup.select(
        'body > div.car-sale-wrap.sale07 > div.carlist-show > div._list-con.list-con.clearfix.ab_carlist > ul > li.con.caritem.conHeight > div.across > a.aimg > div.pad > span:nth-of-type(1)') #nth-of-type(1)取第一个span
    prices = soup.select(
        'body > div.car-sale-wrap.sale07 > div.carlist-show > div._list-con.list-con.clearfix.ab_carlist > ul > li.con.caritem.conHeight > div.across > a.aimg > div.pad > p > em')
    buys = soup.select(
        'body > div.car-sale-wrap.sale07 > div.carlist-show > div._list-con.list-con.clearfix.ab_carlist > ul > li.con.caritem.conHeight > div.across > a.aimg > div.pad > span.pay-price')

    for name, use, price,buy in zip(names, useds, prices,buys):
        data = {
            '名称': name.get_text().strip().replace(' ', '').replace("\n", ""),
            '链接': 'https:'+ name.attrs['href'].strip().replace(' ', '').replace("\n", ""),
            '使用情况': use.get_text().strip().replace(' ', '').replace("\n", ""),
            '价格': price.get_text().strip().replace(' ', '').replace("\n", ""),
            '按揭': buy.get_text().strip().replace(' ', '').replace("\n", "")
        }
        print(data)  # 获取信息并通过字典的信息打印
        f.write("{}\n".format(data))

if __name__ == '__main__':  # 主入口
    urls = ['https://www.xin.com/hangzhou/sn_a24g1h5k0-5v20/i{}/'.format(str(i)) for i in
            range(1, 13)]  # 构造多页url
    for single_url in urls:
        get_links(single_url)  # 循环调用get_links函数
        time.sleep(2)  # 睡眠2秒
    f.close()
