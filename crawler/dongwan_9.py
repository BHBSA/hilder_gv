"""
url = http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/ProjectInfo.aspx?new=1
city : 东莞
CO_INDEX : 9
author: 吕三利
小区数量 : 60    2018/2/24
"""
from crawler_base import Crawler
from lxml import etree
from comm_info import Building, House
import requests
from tool import Tool
from producer import ProducerListUrl


class Dongwan(Crawler):
    def __init__(self):
        self.url = 'http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/ProjectInfo.aspx?new=1'
        self.link_url = 'http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/'

    def start_crawler(self):
        town_list = self.get_town_name()
        view_dict = Tool.get_view_state(self.url,
                                        view_state='//*[@id="__VIEWSTATE"]/@value',
                                        event_validation='//*[@id="__EVENTVALIDATION"]/@value')
        # print(view_dict)
        # print(town_list)
        self.get_all_first_page_url(town_list, view_dict)

    def get_all_first_page_url(self, town_list, view_dict):
        p = ProducerListUrl()
        p.get_current_page_url()
        for i in town_list:
            data = {
                'townName': i,
                '__EVENTVALIDATION': view_dict['__EVENTVALIDATION'],
                '__VIEWSTATE': view_dict['__VIEWSTATE'],
            }
            res = requests.post('http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/ProjectInfo.aspx?new=1', data=data)
            html = etree.HTML(res.content.decode())
            url_list = html.xpath('//*[@id="resultTable"]/tr/td[1]/a/@href')
            complete_url_list = []
            for k in url_list:
                complete_url_list.append('http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/' + k)
            # put in rabbit mq
            self.get_house_url(complete_url_list)
            print(complete_url_list)

    @staticmethod
    def get_house_url(complete_url_list):
        h = House(9)

        p = ProducerListUrl(list_page_url=complete_url_list, request_type='get',
                            current_url_rule='//*[@id="houseTable_1"]/tr[2]/td[2]/a/@href',
                            analyzer_rules_dict=h.to_dict(), analyzer_type='xpath', )
        url_list = p.get_details()

        return url_list

    def get_town_name(self):
        res = requests.get(self.url)
        html = etree.HTML(res.content)
        return html.xpath('//*[@id="townName"]/option/@value')
