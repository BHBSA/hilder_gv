from crawler_base import Crawler
import requests


class Beijing(Crawler):
    def __init__(self):
        self.url = 'http://www.house-book.com.cn/mainAction/c2/%25E5%258C%2597%25E4%25BA%25AC%25E5%25B8%2582.html'

    # def start_crawler(self):
    #     print('继承啦')

    def start(self):
        print('kaishi')
        requests.get(url=self.url)