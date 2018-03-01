"""
有post请求
"""

from crawler_base import Crawler
from comm_info import Comm, Building
from get_page_num import AllListUrl

url = 'http://218.14.207.76/zjfdc3/'
co_index = '69'


class Zhanjiang(Crawler):
    def start_crawler(self):
        all_url = AllListUrl(first_page_url=url, page_count_rule='id="LblPageCount" .*?共 (.*?) 页</span>',
                             analyzer_type='analyzer_type',
                             request_method='get',
                             encode='gbk', )
        page_count = all_url.get_page_count()
        print(page_count)
