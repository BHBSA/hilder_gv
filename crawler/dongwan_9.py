"""
url = http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/ProjectInfo.aspx?new=1
city : 东莞
CO_INDEX : 9
author: 吕三利
小区数量 : 60    2018/2/24
抓不了原因：viewstate中存的数据只能在声明该变量的页面中使用，需要解析js文件
"""
from crawler_base import Crawler
from lxml import etree
from comm_info import Comm, Building, House
import requests, re
from retry import retry


class Dongwan(Crawler):
    def __init__(self):
        self.url = 'http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/ProjectInfo.aspx?new=1'

    def start_crawler(self):
        self.start()

    @retry(retry(3))
    def start(self):
        response = requests.get(self.url)
        html = response.text
        tree = etree.HTML(html)
        building_url_list = tree.xpath('//*[@id="townName"]/option/@value')
        for i in building_url_list:
            print(i)

