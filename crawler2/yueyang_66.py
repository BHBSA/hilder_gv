from comm_info import Comm, Building, House
from crawler_base import Crawler
import requests
import re


class Yueyang(Crawler):
    def __init__(self):
        self.url = 'http://xx.yyfdcw.com/NewHouse/BuildingList.aspx'

    def start_crawler(self):
        page, view_state = self.get_all_page()
        for i in range(1, page + 1):
            post_data = {'__VIEWSTATE': view_state,
                         '__EVENTARGUMENT': page}
            res = requests.post(url='http://xx.yyfdcw.com/NewHouse/BuildingList.aspx', data=post_data)
            print(res.content.decode())

    def get_all_page(self):
        res = requests.get(url=self.url)
        # print(res.content.decode())
        html = res.content.decode()
        page = re.search('当前第./(.*?)页', html, re.S | re.M).group(1)
        view_state = re.search('id="__VIEWSTATE".*?value="(.*?)"', html, re.S | re.M).group(1)
        return int(page), view_state
