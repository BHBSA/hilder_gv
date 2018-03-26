"""
url = gold.ncfdc.com.cn/Default.aspx?tname=251%5cmain
city : 南昌
CO_INDEX : 31
小区数量：254
"""

import requests
from lxml import etree
from producer import ProducerListUrl
from comm_info import Comm, Building, House
import re

url = 'http://gold.ncfdc.com.cn/Default.aspx?tname=251%5cmain'
co_index = '31'
city = '南昌'


class Nanchang(object):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
        }

    def start_crawler(self):
        response = requests.get(url)
        html = response.text
        tree = etree.HTML(html)
        all_comm_url = tree.xpath('//div[@class="lpda_pinyin"]/a/@href')
        self.get_comm_info(all_comm_url)

    def get_comm_info(self, all_comm_url):
        for i in all_comm_url:
            try:
                comm = Comm(co_index)
                comm_url = ('http://gold.ncfdc.com.cn/' + i)
                comm.co_name = 'ctl15_proname">(.*?)<'
                comm.co_address = 'ctl20_ADDRESS">(.*?)<'
                comm.co_develops = 'ctl20_developer_name">(.*?)<'
                comm.co_build_size = 'ctl20_build_area">(.*?)<'
                comm.area = 'ctl20_region_name">(.*?)<'
                comm.co_type = 'ctl20_PropertyType">(.*?)<'
                comm.co_green = 'ctl20_VIRESCENCE">(.*?)<'
                comm.co_volumetric = 'ctl20_PLAT_RATIO">(.*?)<'
                comm.co_id = 'name="form1.*?hrefID=(.*?)"'
                p = ProducerListUrl(page_url=comm_url,
                                    request_type='get', encode='utf-8',
                                    analyzer_rules_dict=comm.to_dict(),
                                    current_url_rule='doc_nav_LD" href="(.*?)"',
                                    analyzer_type='regex',
                                    headers=self.headers)
                build_url_list = p.get_details()
                self.get_build_info(build_url_list)
            except Exception as e:
                print(e)

    def get_build_info(self, build_url_list):
        for i in build_url_list:
            try:
                build = Building(co_index)
                build_url = 'http://gold.ncfdc.com.cn/' + i.replace('amp;', '')
                build.co_name = 'ctl15_proname">(.*?)<'
                build.bu_num = '</tr><tr>.*?<td>.*?<a href=.*?>(.*?)<'
                build.bu_pre_sale = 'onclick="BinSHouseInfo.*?>(.*?)<'
                build.bu_pre_sale_date = 'onclick="BinSHouseInfo.*?<td>(.*?)<'
                build.bu_all_house = 'color:#ec5f00;">(.*?)<'
                build.bu_id = "DisplayB_ld&hrefID=(.*?)'"
                p = ProducerListUrl(page_url=build_url,
                                    request_type='get', encode='utf-8',
                                    analyzer_rules_dict=build.to_dict(),
                                    current_url_rule="</tr><tr>.*?<td>.*?<a href='(.*?)'",
                                    analyzer_type='regex')
                house_url_list = p.get_details()
                self.get_house_info(house_url_list)
            except Exception as e:
                print(e)

    def get_house_info(self, house_url_list):
        for i in house_url_list:
            response = requests.get(i)
            html = response.text
            house_code_list = re.findall("<a href='javascript:void.*?ID='(.*?)'", html)
            for house_code in house_code_list:
                try:
                    house = House(co_index)
                    house_url = 'http://www.ncfdc.com.cn:5060/Module/BB/MyHouseInfo.aspx?bhid=' + house_code
                    # house.ho_num = 'NHOUSENO">(.*?)<'
                    house.ho_name = 'VCHOUSENUM">(.*?)<'
                    house.co_build_structural = 'NHSTRUCTNO_bin">(.*?)<'
                    house.ho_floor = 'CLOCALNUM">(.*?)<'
                    house.ho_build_size = 'NBUILDAREA">(.*?)<'
                    house.ho_true_size = 'HOUSEINSIDE_AREA">(.*?)<'
                    house.ho_type = 'NDESIGN_bin">(.*?)<'
                    house.ho_room_type = 'HOUSETYPE">(.*?)<'
                    house.bu_id = 'NSEATNUM">(.*?)<'
                    p = ProducerListUrl(page_url=house_url,
                                        request_type='get', encode='utf-8',
                                        analyzer_rules_dict=house.to_dict(),
                                        analyzer_type='regex')
                    p.get_details()
                except Exception as e:
                    print(e)
