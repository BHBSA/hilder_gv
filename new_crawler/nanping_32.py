"""
url = http://www.fjnpfdc.com/House/ListCanSell
city : 南平
CO_INDEX : 32
小区数量：254
对应关系：小区：co_name 楼栋：bu_num
"""

import requests
from lxml import etree
from producer import ProducerListUrl
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
import re

url = 'http://www.fjnpfdc.com/House/ListCanSell'
co_index = '32'
city = '南平'


class Nanchang(object):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
        }

    def start_crawler(self):
        b = AllListUrl(first_page_url=url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='gbk',
                       page_count_rule=' 1/(.*?)页',
                       headers=self.headers
                       )
        page = b.get_page_count()
        for i in range(int(page)):
            all_page_url = 'http://www.fjnpfdc.com/House/ListCanSell?page=' + str(i)
            response = requests.get(all_page_url)
            html = response.text
            comm_url_list = re.findall('<tr align="center">.*?<a href="(.*?)"', html, re.S | re.M)
            self.get_comm_info(comm_url_list)

    def get_comm_info(self, comm_url_list):
        for i in comm_url_list:
            comm = Comm(co_index)
            comm_url = 'http://www.fjnpfdc.com/House/' + i
            comm.co_develops = '公司名称：.*?<td.*?>(.*?)<'
            comm.co_pre_sale = '预售许可证：.*?<td.*?>(.*?)<'
            comm.co_name = '项目名称：.*?<td.*?>(.*?)<'
            comm.co_address = '项目坐落：.*?<td.*?>(.*?)<'
            comm.co_use = '规划用途：.*?<td.*?>(.*?)<'
            comm.co_build_size = '建筑面积：.*?<td.*?>(.*?)<'
            comm.co_id = 'ProjectId=(.*?)&'
            p = ProducerListUrl(page_url=comm_url,
                                request_type='get', encode='gbk',
                                analyzer_rules_dict=comm.to_dict(),
                                current_url_rule="<a href='(BuildingInfo.*?)'",
                                analyzer_type='regex',
                                headers=self.headers)
            build_url_list = p.get_details()
            self.get_build_info(build_url_list)

    def get_build_info(self, build_url_list):
        for i in build_url_list:
            build = Building(co_index)
            build_url = 'http://www.fjnpfdc.com/House/' + i
            build.co_name = "项目名称：.*?<td.*?>(.*?)<"
            build.bu_num = "幢　　号：.*?<td.*?>(.*?)<"
            build.co_use = "设计用途：.*?<td.*?>(.*?)<"
            build.co_build_structural = "建筑结构：.*?<td.*?>(.*?)<"
            build.bu_floor = "总 层 数：.*?<td.*?>(.*?)<"
            build.bu_build_size = "总 面 积：.*?<td.*?>(.*?)<"
            build.co_build_end_time = "竣工日期：.*?<td.*?>(.*?)<"
            p = ProducerListUrl(page_url=build_url,
                                request_type='get', encode='gbk',
                                analyzer_rules_dict=build.to_dict(),
                                current_url_rule='<a href="(HouseInfo.*?)"',
                                analyzer_type='regex',
                                headers=self.headers)
            house_url_list = p.get_details()
            self.get_house_info(house_url_list)

    def get_house_info(self, house_url_list):
        for i in house_url_list:
            house = House(co_index)
            house_url = 'http://www.fjnpfdc.com/House/' + i
            house.bu_num = '幢　　号：.*?<td>(.*?)<'
            house.ho_name = '房　　号：.*?<td>(.*?)<'
            house.ho_build_size = '建筑面积：.*?<td>(.*?)<'
            house.ho_true_size = '套内面积：.*?<td>(.*?)<'
            house.ho_share_size = '分摊面积：.*?<td>(.*?)<'
            house.ho_floor = '所 在 层：.*?<td>(.*?)<'
            p = ProducerListUrl(page_url=house_url,
                                request_type='get', encode='gbk',
                                analyzer_rules_dict=house.to_dict(),
                                analyzer_type='regex',
                                headers=self.headers)
            p.get_details()
