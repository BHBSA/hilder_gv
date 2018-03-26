"""
url = http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/ProjectInfo.aspx?new=1
city : 东莞
CO_INDEX : 9
author: 吕三利
小区数量 : 60    2018/2/24

2018/3/9 少区域

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
        self.co_index = 9

    def start_crawler(self):
        town_list = self.get_town_name()
        print(town_list)
        view_dict = Tool.get_view_state(self.url,
                                        view_state='//*[@id="__VIEWSTATE"]/@value',
                                        event_validation='//*[@id="__EVENTVALIDATION"]/@value')
        # print(view_dict)
        # print(town_list)
        all_building_url_list = self.get_all_first_page_url(town_list, view_dict)
        print(all_building_url_list)

        house_url_list = self.get_build_detail(all_building_url_list)

        self.get_house_detail(house_url_list)

    @staticmethod
    def get_house_detail(house_url_list):
        print(house_url_list)
        for i in house_url_list:
            h = House(9)
            h.bu_num = '项目名称.*?>(.*?)（<'  # 项目名称
            h.ho_name = 'target=\'_blank\'>(.*?)</a>'
            h.info = '建筑面积：.*?</a></td>'
            p = ProducerListUrl(page_url=i,
                                request_type='get',
                                analyzer_rules_dict=h.to_dict(),
                                analyzer_type='regex', )
            p.get_details()
        print('房号放入完成')

    @staticmethod
    def get_build_detail(all_building_url_list):
        house_url_list = []
        for i in all_building_url_list:
            b = Building(9)
            b.bo_develops = '//*[@id="content_1"]/div[3]/text()[2]'  # 开发商
            b.bu_num = '//*[@id="content_1"]/div[3]/text()[3]'  # 项目名称
            b.bu_build_size = '//*[@id="houseTable_1"]/tr[2]/td[6]/a/text()'  # 销售面积
            b.bu_pre_sale = '//*[@id="houseTable_1"]/tr[2]/td[1]/a/text()'  # 预售证书
            b.bu_address = '//*[@id="houseTable_1"]/tr[2]/td[2]/a/text()'  # 坐落
            b.bu_floor = '//*[@id="houseTable_1"]/tr[2]/td[3]/a/text()'  # 总层数
            b.bu_all_house = '//*[@id="houseTable_1"]/tr[2]/td[4]/a/text()'  # 总套数
            b.bu_type = '//*[@id="houseTable_1"]/tr[2]/td[5]/a/text()'  # 房屋用途
            p = ProducerListUrl(page_url=i, request_type='get',
                                current_url_rule='//*[@id="houseTable_1"]/tr[2]/td[2]/a/@href',
                                analyzer_rules_dict=b.to_dict(), analyzer_type='xpath', )
            url_list = p.get_details()
            complete_url = []
            for k in url_list:
                complete_url.append('http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/' + k)
            house_url_list = complete_url + house_url_list
        return house_url_list

    @staticmethod
    def get_all_first_page_url(town_list, view_dict):
        all_building_url_list = []
        for i in town_list:
            try:
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
                all_building_url_list = all_building_url_list + complete_url_list
            except Exception as e:
                print(e)
                continue
        return all_building_url_list

    def get_town_name(self):
        res = requests.get(self.url)
        html = etree.HTML(res.content)
        return html.xpath('//*[@id="townName"]/option/@value')
