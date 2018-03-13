"""
url = http://www.cxsfdcglzx.com/touming/wangShangHouse.aspx
city : 慈溪（宁波）
CO_INDEX : 8
author: 吕三利
小区数量 : 1901    2018/2/24
"""

from crawler_base import Crawler
from lxml import etree
from comm_info import Comm, Building, House
import requests, re
from retry import retry
import yaml
from lib.mongo import Mongo

setting = yaml.load(open('config_local.yaml'))
CO_ID = 0


class Ningbo(Crawler):
    def __init__(self):
        self.url = 'http://www.cxsfdcglzx.com/touming/wangShangHouse.aspx'

    def start_crawler(self):
        self.start()

    def is_none(self, xpath_adv):
        if xpath_adv:
            xpath_adv = xpath_adv[0]
        else:
            xpath_adv = None
        return xpath_adv

    @retry(retry(3))
    def start(self):
        response = requests.get(self.url)
        html = response.text
        tree = etree.HTML(html)
        comm_url_list = tree.xpath('//ul[@class="NewsList"]/li/a/@href')
        for i in comm_url_list:
            comm = Comm(8)
            comm_url = 'http://www.cxsfdcglzx.com/touming/' + i
            print(comm_url)
            self.get_comm_info(comm_url, comm)

    @retry(retry(3))
    def get_comm_info(self, comm_url, comm):
        try:
            response = requests.get(comm_url)
            html = response.text
            tree = etree.HTML(html)
            co_address = tree.xpath('//*[@id="PageB_Location"]/text()')[0]  # 小区地址
            co_develops = tree.xpath('//*[@id="PageB_CompName"]/text()')[0]  # 开发商
            co_pre_sale = tree.xpath('//*[@id="PageB_PermitNo"]/text()')[0]  # 预售证书
            co_build_end_time = tree.xpath('//*[@id="PageB_FinishDate"]/text()')[0]  # 竣工时间
            co_build_size = tree.xpath('//*[@id="PageB_BuildArea"]/text()')[0]  # 建筑面积
            build_url_list = tree.xpath('//*[@id="Content"]/div[3]/div/div[4]/div[3]/table[2]/tr/td[1]/a/@href')
            comm.co_address = co_address
            comm.co_develops = co_develops
            comm.co_pre_sale = co_pre_sale
            comm.co_build_end_time = co_build_end_time
            comm.co_build_size = co_build_size
            for i in build_url_list:
                building = Building(8)
                url = 'http://www.cxsfdcglzx.com/touming/' + i
                print(url)
                self.get_build_info(url, comm, building)
        except BaseException as e:
            print(e)


    @retry(retry(3))
    def get_build_info(self, url, comm, building):
        try:
            coll = Mongo(setting['db'], setting['port'], setting['db_name'],
                         setting['coll_comm']).get_collection_object()
            response = requests.get(url)
            html = response.text
            tree = etree.HTML(html)
            co_name = tree.xpath('//*[@id="PageB_Location"]/text()')[0]  # 小区名字
            print(co_name)
            bu_name = tree.xpath('//*[@id="ItemName"]/text()')[0]  # 楼栋名称
            bu_num = tree.xpath('//*[@id="PageB_HouseNo"]/text()')[0]  # 楼号 栋号
            bu_all_house = tree.xpath('//*[@id="lb_countbulidtaoshu"]/text()')[0]  # 总套数
            bu_floor = tree.xpath('//*[@id="cell3-1"]/text()')
            bu_floor = self.is_none(bu_floor)  # 楼层
            bu_build_size = tree.xpath('//*[@id="lb_countbulidarea"]/text()')[0]  # 建筑面积
            bu_live_size = tree.xpath('//*[@id="lb_buildarea"]/text()')[0]  # 住宅面积
            bu_price = tree.xpath('//*[@id="lb_buildavg"]/text()')
            bu_price = self.is_none(bu_price)  # 住宅价格
            bu_id = re.search('\?(\d+)$', url).group(1)  # 楼栋id
            building.co_id = CO_ID
            building.bu_name = bu_name
            building.bu_num = bu_num
            building.bu_all_house = bu_all_house
            building.bu_floor = bu_floor
            building.bu_build_size = bu_build_size
            building.bu_live_size = bu_live_size
            building.bu_price = bu_price
            building.bu_id = bu_id
            house_info_list = tree.xpath('//td[@oncontextmenu="return false"]/*/text()')
            count = 0
            house = House(8)
            for i in house_info_list:
                if count % 4 == 0:
                    ho_name = i.replace('<', '').replace('>', '')
                    house.ho_name = ho_name
                elif count % 4 == 1:
                    ho_true_size = i
                    house.ho_true_size = ho_true_size
                elif count % 4 == 2:
                    co_type = i
                    comm.co_type = co_type
                count += 1
                if count % 4 == 0:
                    house.co_id = CO_ID
                    house.bu_id = bu_id
                    house.insert_db()
                    house = House(8)
            comm_list = coll.find_one({'co_name': co_name})
            if not comm_list:
                global CO_ID
                CO_ID += 1
                building.bu_id = bu_id
                comm.co_name = co_name
                comm.co_id = CO_ID
                comm.insert_db()
            building.insert_db()
        except BaseException as e:
            print(e)

