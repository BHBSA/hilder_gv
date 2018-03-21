"""
url = http://www.sxyqfdc.com:85/More_xm.aspx
city :  阳泉
CO_INDEX : 62
author: 程纪文
"""

from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import re, requests
from lxml import etree
import json

co_index = 62

class Yangjiang(Crawler):
    def __init__(self):
        self.url = "http://www.sxyqfdc.com:85/"
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36', }
        self.page = 7
    def start_crawler(self):
        for i in range(1,self.page):
            url = self.url +"More_xm.aspx?page=" +str(i)
            p = ProducerListUrl(page_url=url,
                                request_type='get', encode='utf-8',
                                analyzer_rules_dict=None,
                                current_url_rule="//td[@align='left']/a/@href",
                                analyzer_type='xpath',
                                headers=self.headers)
            comm_url_list = p.get_current_page_url()
            self.get_comm_info(comm_url_list)


