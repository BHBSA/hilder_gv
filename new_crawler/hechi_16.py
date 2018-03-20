from crawler_base import Crawler
import requests
import re
from tool import Tool
from lxml import etree


class Hechi(Crawler):
    def __init__(self):
        self.url = 'http://www.hcsfcglj.com/Templets/BoZhou/aspx/spflist.aspx'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Cookie': 'ASP.NET_SessionId=lllitzrxbio3mh2s1gpmrhmg',
            'Referer': 'http://www.hcsfcglj.com/Templets/BoZhou/aspx/spflist.aspx'
        }

    def start_crawler(self):
        view_info = Tool.get_view_state(url=self.url,
                                        view_state='//*[@id="__VIEWSTATE"]/@value',
                                        event_validation='//*[@id="__EVENTVALIDATION"]/@value')
        page_count = self.get_page_count()
        self.get_all_detail_url(page_count, view_info)

    def get_all_detail_url(self, page_count, view_info):
        url_list = []

        for i in range(1, page_count + 1):
            post_data = {'navigate$txtNewPageIndex': str(i),
                         '__VIEWSTATE': view_info['__VIEWSTATE'],
                         '__EVENTVALIDATION': view_info['__EVENTVALIDATION'],
                         '__EVENTTARGET': 'navigate$LnkBtnNext',
                         '__EVENTARGUMENT': None,
                         'txt_developer': None,
                         'txt_code': None,
                         'txt_address': None,
                         'txt_Name': None}
            res = requests.post(url=self.url, data=post_data, headers=self.headers)

            print(res.content.decode())
        return url_list

    def get_page_count(self):
        res = requests.get(self.url)
        html_str = res.content.decode()
        count = re.search('navigate_LblPageCount">(.*?)</span>', html_str, re.S | re.M).group(1)
        return int(count)
