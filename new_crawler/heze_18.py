"""
url = http://www.hzszjj.gov.cn/ts_web_dremis/web_house_dir/Show_GoodsHouse_More.aspx
city : 菏泽
CO_INDEX : 18
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

url = 'http://www.hzszjj.gov.cn/ts_web_dremis/web_house_dir/Show_GoodsHouse_More.aspx'
co_index = '18'
city = '菏泽'


class Heze(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
        }

    def start_crawler(self):
        b = AllListUrl(first_page_url=url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='utf-8',
                       page_count_rule="下一页.*?AspNetPager1','(.*?)'",
                       )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            view_dict = Tool.get_view_state(url,
                                            view_state='//*[@id="__VIEWSTATE"]/@value',
                                            event_validation='//*[@id="__EVENTVALIDATION"]/@value')
            data = {
                'townName': i,
                '__EVENTVALIDATION': view_dict['__EVENTVALIDATION'],
                '__VIEWSTATE': view_dict['__VIEWSTATE'],
            }
            self.get_all_url_comm(data)

    def get_all_url_comm(self, data):
        p = ProducerListUrl(page_url=url,
                            request_type='post', encode='utf-8',
                            analyzer_rules_dict=anlyzer_dict,
                            analyzer_type='regex',
                            headers=self.headers,
                            post_data=data)
