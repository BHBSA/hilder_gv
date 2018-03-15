"""
url = http://183.63.60.194:8808/public/web/index
city : 河源
CO_INDEX : 17
author:
小区数量：
"""

from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import re, requests
from urllib import parse
from tool import Tool

url = 'http://183.63.60.194:8808/public/web/index'
co_index = '17'
city = '河源'


class Heyuan(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
        }

    def start_crawler(self):
        b = AllListUrl(first_page_url=url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='utf-8',
                       page_count_rule='id="lblPageCount">(.*?)<',
                       )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            info_url = 'http://183.63.60.194:8808/api/GzymApi/GetIndexSearchData?' \
                       'Jgid=FC830662-EA75-427C-9A82-443B91E383CB&PageIndex=' + str(i) + \
                       '&PageSize=100&Ysxmmc=&Ysxkzh=&Kfsmc=&Kfxmmc='
            comm = Comm(co_index)
            comm.co_name = 'KFQYMC":"(.*?)"'
            anlyzer_dict = comm.to_dict()
            p = ProducerListUrl(page_url=info_url,
                                request_type='get', encode='utf-8',
                                analyzer_rules_dict=anlyzer_dict,
                                analyzer_type='regex',
                                headers=self.headers)
            p.get_details()


if __name__ == '__main__':
    h = Heyuan()
    h.start_crawler()
