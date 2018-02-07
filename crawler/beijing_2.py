"""
url: http://www.bjjs.gov.cn/eportal/ui?pageId=307678
city: 北京
CO_INDEX: 2
"""
from crawler_base import Crawler
import requests


class Beijing(Crawler):
    def __init__(self):
        self.url = 'http://www.bjjs.gov.cn/eportal/ui?pageId=307678'

    # def start_crawler(self):
    #     print('继承啦')

    def start(self):
        print('kaishi')
        requests.get(url=self.url)