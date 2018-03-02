"""
url = http://www.tmsf.com/newhouse/property_searchall.htm
city: 百色
CO_INDEX: 15
author: 周彤云
小区数：2065
time:2018-03-02
"""

CO_INDEX = 15
import requests
from lxml import etree
from comm_info import Comm, Building, House
from crawler_base import Crawler
import re
from retry import retry


class Hangzhou(Crawler):
    def __init__(self):
        self.url = 'http://www.tmsf.com/newhouse/property_searchall.htm?searchkeyword=&keyword=&sid=&districtid=&areaid=&dealprice=&propertystate=&propertytype=&ordertype=&priceorder=&openorder=&view720data=&page=1&bbs=&avanumorder=&comnumorder='

    def start_crawler(self):
        self.start()

    @retry(tries=3)
    def get_all_page(self):
        try:
            res = requests.get(url=self.url)
            html = res.content.decode('gb2312', 'ignore').replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
            page = re.search(r'class="green1">1/(\d+)</font>', html).group(1)
            # print(page)
            return page
        except Exception as e:
            print('retry')
            raise

    @retry(tries=3)
    def start(self):
        page = self.get_all_page()
        for i in range(1, int(page)+1):
            res = requests.get()




if __name__ == '__main__':
    b = Hangzhou()
    b.start_crawler()
