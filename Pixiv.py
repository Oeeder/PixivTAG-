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
            'path': '/tags/TouhouProject',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': 'first_visit_datetime_pc=2020-09-11+19:37:59; p_ab_id=0; p_ab_id_2=8; p_ab_d_id=2016959911; __utmz=235335808.1599820679.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided); yuid_b=NlBIcUE; _ga=GA1.2.1837632309.1599820679; c_type=21; a_type=1; b_type=1; login_ever=yes; privacy_policy_agreement=2; ki_r=; PixivPreview={"lang":"-1","enablePreview":1,"enableSort":1,"enableAnimeDownload":1,"original":0,"previewDelay":200,"pageCount":20,"favFilter":0,"hideFavorite":0,"hideFollowed":0,"linkBlank":1,"pageByKey":0,"version":"3.2.0"}; adr_id=RYzL4LxGlctWXBUjq21alsYWnYya4ILuuuAnDB2ZqrfKHKoc; categorized_tags=4lLoPnomZL~6sZKldb07K~BeQwquYOKY~CADCYLsad0~DN6RDM1CuJ~EoUihEZSHs~RsIQe1tAR0~Z8Y-yg1SLv~_bee-JX46i~aLBjcKpvWL~b8b4-hqot7~bXMh6mBhl8~flsfhfUnHV~kL195qN6Br~kP7msdIeEU~kY01H5r3Pd~m3EJRa33xU; ki_s=214027:0.0.0.0.2;214908:0.0.0.0.2;214994:0.0.0.0.2;215190:0.0.0.0.2;215821:0.0.0.0.2; __gads=ID=ff9b1d21b57879cf:T=1620901811:S=ALNI_MZQD2QKUHRK0LbzKv5zDDwwxGhW9w; PHPSESSID=14637724_oGe8YskUGiHlBLRyFnwLdqXdgjkyrEqI; device_token=8fe95b9cf434b42811268dbe103aadc8; privacy_policy_notification=0; __utma=235335808.1837632309.1599820679.1622103185.1623350756.21; __utmc=235335808; tags_sended=1; tag_view_ranking=ob1ETnC6B5~zIv0cf5VVk~RTJMXD26Ak~m3EJRa33xU~kCtgd6tAEn~0xsDLqCEW6~EoUihEZSHs~XpYOJt3r5W~JTw4P9HqBt~BEa426Zwwo~mdxz-DAWvt~engSCj5XFq~yqhVAkZ_Lh~Lt-oEicbBr~UXED5byh-c~_bee-JX46i~aLBjcKpvWL~Ie2c51_4Sp~KL71C9NfGw~QAc5ZnUp3f~K8esoIs2eW~2QTW_H5tVX~xXzk6DCo23~ETjPkL0e6r~NLzv9xwLl_~KEeQ-HJLi_~C39dEX5PzS~5bL8jjxrCT~U-RDdr1VQk~ddxL6zw1bS~m_9cqJoLdX~Xyw8zvsyR4~uusOs0ipBx~jhuUT0OJva~WVrsHleeCL~lRHALpj_iJ~DjehokSFFa~3gc3uGrU1V~kxhAdvEiVl~KLnB8J4tVu~uEnluKUIo7~ixFiTdvm6E~fbUyQrXMR3~LJo91uBPz4~ES26rBEjpu~yWFDgVYfAy~ELtJ0EUcAp~1tYSAyYhof~i6_HYia-I3~rZ1Xexbx2-~sm2KG7bpS8~xdkteyto76~CBp3gUdA4D~sKs0aPaW87~lH5YZxnbfC~kGYw4gQ11Z~37dsYFfqRK~CBhkSh6lt_~05XvkINl3k~klhaD7RvNc~HBlflqJjBZ~1He38OZ0Xy~nAtxkwJ5Sy~fUS-Ay2M9Z~Vc8Zqe9nWr~y92Sf_2CTx~np4_dDk1-Q~sFgThrAAKl~n6KI9n0v4T~2-ZLcTJsOe~AMwBN_-Fo_~MRvyDIZDJL~K0rZerf8iy~jUfFWSG39-~sOBG5_rfE2~cFYMvUloX0~NhbGhFqydR~jH0uD88V6F~m1cBGlIsY3~FWiiNBn8_g~csE6L2Z7_c~8H_bi3nVqy~VbPCYJXdEP~5f1R8PG9ra~HY55MqmzzQ~V06ijX-Hk0~_hSAdpN9rx~bXMh6mBhl8~0FVTjW267s~qioIDQfvek~vG2wxYo31C~nJ2x05fDoI~ZzvSS1eDcs~LtW-gO6CmS~OT4SuGenFI~kP7msdIeEU~kL195qN6Br~0c-czF-PqM~z4HDQFTejn~flsfhfUnHV; _im_vid=01F7VM37S06AFQ48T4QN2QYJSA; _im_uid.3929=b.997af5284fefe8d4; first_visit_datetime=2021-06-11+04:19:03; webp_available=1; __utmv=235335808.|2=login ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=14637724=1^9=p_ab_id=0=1^10=p_ab_id_2=8=1^11=lang=zh=1^20=webp_available=yes=1; __utmt=1; OX_plg=pm; _gid=GA1.2.1319328480.1623352757; cto_bundle=aOWBo19NUDlBWGJvNkVYM2FWWkpZV1cweUJDRnpzZHF2bEhWOXNDbUJuNVolMkJHa2M4NTVEMG5Vd0VaTnVCcERQWjFSZlFibFQ3alAlMkZTdEVKZyUyRlRYMU1UUW9IQ2gycXltZFNzZSUyRmZhSFIybGp4eXVGVFRVZ1B4bmM0dVFYRTF2ZXI2VjFoZ29NQVJURG1ic3A4YUtBMyUyQllaWlRBJTNEJTNE; limited_ads={"t_footer":"11615"}; __cf_bm=a0cbb8383ac4107a38574e1eec81e74f2a8e284e-1623353174-1800-AXRNw1vTLf5u0JhAeaxGdZnZeoXcR6evh9Q9omR2wUGI6ec4KnlgAbBY5c3I5WbP9zFmdfL/ZTJsclsTAerk4tvmpQGqsUD/ckTZe1FEjku0YkPBGa3z0IpMPOZaUnMG2UQTmJRGoQBzIKTRQILLadPwCwELNhSHrjDrpgls4081msRb1X0teo8xePtmVENHaw==; __utmb=235335808.13.9.1623352763924; ki_t=1602727169327;1623350758710;1623353176143;15;103',
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
        chrome_options.add_argument('--headless')#后台运行
        chrome_options.add_argument('--disable-gpu')                            #后台运行
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
    folder = "C:\\Users\\mcmo\\Desktop\\TEST\\PYTHON\\PixivPiture\\"+"PixivDaily"+tagname+year+month+day #保存文件夹的路劲
    if not os.path.exists(folder):  # 不存在文件夹时，制作
        os.makedirs(folder)
    f = open(folder + '/%s.%s' % (str(img_id), original_url.group(1)[-3:]), 'wb')  # 将图像保存到PixivDaily文件夹
    f.write(img.content)
    f.close()


if __name__ == "__main__":
    main()
