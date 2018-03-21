"""
url = http://113.106.199.148/web/presale.jsp?page=2
city : 惠州
CO_INDEX : 21
author: 吕三利
小区数量：401
"""

from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import re, requests
from urllib import parse
from tool import Tool

url = 'http://113.106.199.148/web/presale.jsp?page=1'
co_index = '21'
city = '惠州'


class Huizhou(Crawler):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
        }

    def start_crawler(self):
        b = AllListUrl(first_page_url=url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='gbk',
                       page_count_rule='第1页 / 共(.*?)页',
                       )
        page = b.get_page_count()
        all_url_list = []
        for i in range(1, int(page) + 1):
            all_url = 'http://113.106.199.148/web/presale.jsp?page=' + str(i)
            comm_url_list = self.get_comm_url(all_url)
            all_url_list += comm_url_list
        all_comm_url_list = []
        for i in all_url_list:
            tool = Tool()
            replace_str = tool.url_quote(i, encode='gbk')
            comm_url = 'http://113.106.199.148/web/' + replace_str
            build_list = self.get_comm_info(comm_url)
            all_comm_url_list += build_list
        build_all_list = []
        for i in all_comm_url_list:
            build_url = 'http://113.106.199.148/web/' + str(i)
            house_list = self.get_build_info(build_url)
            build_all_list += house_list
        house_all_list = []
        bu_id_list = []
        for i in build_all_list:
            code = i.split(',')
            house_url = "http://113.106.199.148/web/House.jsp?id=" + code[0] + "&lcStr=" + code[1]
            house_all_list.append(house_url)
            bu_id_list.append(code[0])
        self.get_house_info(house_all_list, bu_id_list)

    def get_house_info(self, house_all_list, bu_id_list):
        count = 0
        for i in bu_id_list:
            house = House(co_index)
            house_url = house_all_list[count]
            count += 1
            response = requests.post(house_url)
            html = response.content.decode('gbk')
            house.bu_id = i
            house.ho_floor = re.search('所在楼层：.*?<td>(.*?)<', html, re.M | re.S).group(1)
            house.ho_name = re.search('房号：.*?<td>(.*?)<', html, re.M | re.S).group(1)
            house.ho_build_size = re.search('预测总面积：.*?<td>(.*?)<', html, re.M | re.S).group(1)
            house.ho_true_size = re.search('预测套内面积.*?<td>(.*?)<', html, re.M | re.S).group(1)
            house.ho_share_size = re.search('预测套内面积.*?<td>(.*?)<', html, re.M | re.S).group(1)
            house.insert_db()

    def get_build_info(self, all_build_url_list):
        p = ProducerListUrl(page_url=all_build_url_list,
                            request_type='get', encode='gbk',
                            current_url_rule="onclick=' openContent\((.*?)\)",
                            analyzer_rules_dict=None,
                            analyzer_type='regex',
                            headers=self.headers)
        house_url_list = p.get_current_page_url()
        return house_url_list

    def get_comm_url(self, all_url):
        p = ProducerListUrl(page_url=all_url,
                            request_type='get', encode='gbk',
                            current_url_rule='align="center">&nbsp;<a href=".*?target="_blank">.*?<td>&nbsp;<a href="(.*?)".target="_blank">',
                            analyzer_rules_dict=None,
                            analyzer_type='regex',
                            headers=self.headers)
        comm_url_list = p.get_current_page_url()
        return comm_url_list

    def get_comm_info(self, all_comm_url_list):
        c = Comm(co_index)
        c.co_id = 'jectcode=(.*?)"'
        c.co_name = "项目名称：</th>.*?<td.*?>(.*?)<"
        c.co_address = '项目地址：</th>.*?<td.*?>(.*?)<'
        c.co_develops = '开发企业：</th>.*?<td.*?>(.*?)<'
        c.co_pre_sale = '资质证书编号：</th>.*?<td.*?>(.*?)<'
        c.co_owner = '国土证书：</th>.*?<td.*?>(.*?)<'
        c.co_build_structural = '<td align="center">.*?center.*?center">(.*?)<.*?center'
        c.area = '行政区划：</th>.*?<td.*?>(.*?)<'
        b = Building(co_index)
        b.co_id = 'jectcode=(.*?)"'
        b.bu_id = 'buildingcode=(.*?)&'
        b.bu_floor = 'center.*?center.*?center.*?center.*?center">(.*?)<.*?"center'
        b.bu_all_house = 'center.*?center.*?center.*?center(.*?)center">.*?<.*?"center'
        b.bu_num = 'center.*?center(.*?)center.*?center.*?center">.*?<.*?"center'
        data_list_comm = c.to_dict()
        p_comm = ProducerListUrl(page_url=all_comm_url_list,
                                 request_type='get', encode='gbk',
                                 analyzer_rules_dict=data_list_comm,
                                 current_url_rule='align="center"><a href="(.*?)" target="_blank".*?查看信息',
                                 analyzer_type='regex',
                                 headers=self.headers)
        p_comm.get_details()
        data_list_build = b.to_dict()
        p_bu = ProducerListUrl(page_url=all_comm_url_list,
                               request_type='get', encode='gbk',
                               analyzer_rules_dict=data_list_build,
                               current_url_rule='align="center"><a href="(.*?)" target="_blank".*?查看信息',
                               analyzer_type='regex',
                               headers=self.headers)
        house_list = p_bu.get_details()
        return house_list
