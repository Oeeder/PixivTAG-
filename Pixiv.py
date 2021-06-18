#/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8
# @Time : 2021/6/18
# @Oeed
# 参考项目：https://github.com/Karasukaigan/pixiv-get-daily

import time
import requests
import re
import os
import json
from lxml import etree
from lxml import html
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import urllib
import urllib.parse
import random
import re
from distutils.filelist import findall
import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver

from io import BytesIO
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib import request
from io import BytesIO
from requests import get
import gzip
import time
from selenium.webdriver.common.by import By

tagname = input("请输入搜索的TAG词条")
print(tagname)
page = input("搜索的页数")
print(page)
pager = int(page)+1
def main():
    for i in range(1, 2):  #1循环下载50张图像，循环10次
        allimg_id = get_img_id(i)  # 取图像ID
        for j in range(0, len(allimg_id)):
            download_img(allimg_id[j])  # 通过ID下载图像
            n = j + 1
            print("(" + str(i) + "/10),(" + str(n) + "/" + str(len(allimg_id)) + ")")  # 显示进度情况
            time.sleep(1)  # 为了不增加服务器的负荷，适当设定待机时间，单位为秒

def get_img_id(a):
    id_down = []
    for pages in range(1, pager):
        headers = {
            'authority': 'www.pixiv.net',
            'method': 'GET',
            'path': '/tags/', + tagname
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': '',#请自行放入cookie
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
        }

        profile_dir = r'C:\Users\mcmo\AppData\Local\Google\Chrome\User Data\Default'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')#ROOT权限
        chrome_options.add_argument("user-data-dir=" + os.path.abspath(profile_dir))#后台运行
        chrome_options.add_argument('--headless')                                   #后台运行
        chrome_options.add_argument('--disable-gpu')                                #后台运行，如需要进行测试，请把这3行后台运行注释掉
        browser = webdriver.Chrome(chrome_options=chrome_options)#浏览器启动
        time.sleep(5)
        url = 'https://www.pixiv.net/tags/' + tagname + '/illustrations?' + 'mode=safe' + '&p=' + str(pages)
        print(url)
        browser.get(url)
        for i in range(1, 8):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')#模拟浏览器操作 拉到最下
        time.sleep(1)

        soup = BeautifulSoup(browser.page_source, 'lxml')#网页源代码
        soups = soup.prettify()#自动换行
        text = etree.HTML(soups)#转换ETREE格式

        p_list = text.xpath('//a[@data-gtm-value and @class="rp5asc-16 kdmVAX sc-AxjAm MksUu"]')  # 定位元素

        id_list = []
        for index in range(len(p_list)):#定位ID
            if (index % 1) == 0:
                print(p_list[index].attrib)
                id = p_list[index].attrib
                id_list.append(id['data-gtm-value'])  # 1
        browser.quit()

        for indes in range(len(id_list)):#根据收藏数定位ID
            if (index % 1) == 0:
                url = "https://www.pixiv.net/artworks/" + str(id_list[indes])
                response = requests.get(url, headers=headers)
                all_img_id = re.findall('"bookmarkCount":(\d+?),', response.text)
                if int(all_img_id[0]) > 100:#收藏数
                    id_down.append(id_list[indes])
                print(id_down)
    return id_down

def download_img(img_id):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,ja;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "referer": "https://www.pixiv.net/ranking.php?mode=daily",
    }

    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('localtime=' + localtime)
    # 系统当前时间年份
    year = time.strftime('%Y', time.localtime(time.time()))
    # 月份
    month = time.strftime('%m', time.localtime(time.time()))
    # 日期
    day = time.strftime('%d', time.localtime(time.time()))

    img_url = "https://www.pixiv.net/artworks/" + str(img_id)
    response = requests.get(img_url, headers=headers)  # 请求特定图像页面
    original_url = re.search('"original":"(.+?)"},"tags"', response.text)  # 寻找原始图像的URL
    img = requests.get(original_url.group(1), headers=headers)  # 请求原始图像
    folder = "PixivDaily"+tagname+year+month+day #保存文件夹的路径
    if not os.path.exists(folder):  # 不存在文件夹时，创建文件夹
        os.makedirs(folder)
    f = open(folder + '/%s.%s' % (str(img_id), original_url.group(1)[-3:]), 'wb')  # 将图像保存到PixivDaily文件夹
    f.write(img.content)
    f.close()


if __name__ == "__main__":
    main()
