"""
url:http://www.gzbjfc.com/House.aspx
city: 毕节
CO_INDEX: 3
author : j
"""
import requests
from crawler_base import Crawler
from comm_info import Comm, Building, House
from retry import retry
from lxml import etree

CO_INDEX = 3


class Bijie(Crawler):
    def __init__(self):
        self.start_url = 'http://www.gzbjfc.com/House.aspx'

    @retry(retry(3))
    def start_crawler(self):
        res = requests.get(url=self.start_url)

        # 获取所有分页的url
        url_list = self.get_all_comm_list_url(res.content.decode())
        self.crawler_comm_url(url_list)

    # @retry(retry(3))
    def crawler_comm_url(self, url_list):
        # 请求所有的小区列表页面
        for i in url_list:
            c = Comm()
            res = requests.get(i)
            html = etree.HTML(res.content.decode())
            c.co_name = html.xpath(
                '//*[@id="form1"]/div/div[2]/div[2]/div[3]/div[2]/table[1]/tbody/tr/td/table/tbody/tr[1]/td[2]/div/a')
            print(c.co_name)
            break


@staticmethod
def get_all_comm_list_url(page):
    """

    :param page: 首页html
    :return: url list
    """
    comm_list = []
    html = etree.HTML(page)
    page_num = int(html.xpath('//*[@id="cph_hl1_pagerTop"]/a[12]')[0].attrib['href'].split('page=')[1])
    print(page_num)
    for i in range(1, page_num + 1):
        comm_list.append('http://www.gzbjfc.com/House.aspx?page=' + str(i))

    print(comm_list)
    return comm_list
