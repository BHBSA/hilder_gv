from crawler_base import Crawler
from comm_info import Comm, Building
from get_page_num import AllListUrl
from producer import ProducerListUrl
import requests

url = 'http://www.gyfc.net.cn/2_proInfo/index.aspx'
co_index = '13'


class Guiyang(Crawler):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
        }

    def start_crawler(self):
        all_url = AllListUrl(first_page_url=url, page_count_rule='总页数.*?<b>(.*?)</b>',
                             analyzer_type='regex',
                             request_method='get',
                             headers=self.headers,
                             encode='gbk')
        page_count = all_url.get_page_count()
        all_url_list = []
        for i in range(1, page_count + 1):
            all_url_list.append('http://www.gyfc.net.cn/2_proInfo/index.aspx/page=' + str(i))
        print(all_url_list)

        comm_detail_page = self.get_comm_info(all_url_list)
        print(comm_detail_page)

    def get_comm_info(self, all_url_list):
        c = Comm(co_index)
        c.co_name = '//*[@id="right"]/table/tr/td/div/table/tr/td/table/tr[1]/td[3]'
        data_list = c.to_dict()

        g = ProducerListUrl(list_page_url=all_url_list, request_type='get', encode='gbk',
                            current_url_rule='//*[@id="right"]/table/tr/td/div/table/tr/td[1]/table/tr[1]/td[1]/a/@href',
                            analyzer_rules_dict=data_list, analyzer_type='xpath', headers=self.headers)
        url_list = g.get_details()
        return url_list
