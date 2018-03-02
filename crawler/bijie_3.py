"""
url:http://www.gzbjfc.com/House.aspx
city: 毕节
CO_INDEX: 3
author : 周彤云
小区数：660
time:2018-02-11
"""
CO_INDEX = 3
import requests
from crawler_base import Crawler
from comm_info import Comm, Building, House
from retry import retry
from lxml import etree

class Bijie(Crawler):
    def __init__(self):
        self.start_url = 'http://www.gzbjfc.com/House.aspx'

    def start_crawler(self):
        self.bijie_start()

    @retry(retry(3))
    def get_all_page(self):
        try:
            res = requests.get(url=self.start_url)
            html = res.content.decode()
            # print(html)
            tree = etree.HTML(html)
            #获取总页数
            page =tree.xpath('//div[@id="cph_hl1_pager"]/a[12]/@href')[0].split('=')[1]
            return page
        except Exception as e:
            print('retry')
            raise

    @retry(retry(3))
    def bijie_start(self):
        try:
            page = self.get_all_page()
            for i in range(1, int(page)+1):
                # print(i)
                res = requests.get(self.start_url+'?page=' + str(i))
                html = res.content
                tree = etree.HTML(html)
                # print(res)
                #获取每一页小区列表的url
                comm_list =tree.xpath('//table[@class="Repeater"]//div[@align="left"]/a[@class="url"]/@href')
                # print(comm_list)
                for i in comm_list:
                    comm = Comm()
                    comm_url = 'http://www.gzbjfc.com' + i
                    # print(comm_url)
                    comm_obj = self.get_comm_detail(comm_url)
                    # comm_obj.insert_db()
        except Exception as e:
            print('retry')
            raise


    @retry(retry(3))
    def get_comm_detail(self, comm_url):
        try:
             res = requests.get(url=comm_url)
             co_id = res.url
             print(co_id)
             html = res.content.decode()
             tree = etree.HTML(html)
             # 获取小区页面字段
             co_name = tree.xpath('//span[@id="cph_hif1_xmmc"]/font/text()')[0]  # 小区名称
             # print(co_name)
             co_pre_sale = tree.xpath('//span[@id="cph_hif1_xsxkz"]/font/text()')[0]  # 预售证书
             # print(co_pre_sale)
             co_address = tree.xpath('//span[@id="cph_hif1_zl"]/font/text()')[0]  # 小区地址
             # print(co_address)
             co_develops = tree.xpath('//span[@id="cph_hif1_kfs"]/font/text()')[0]  # 开发商
             # print(co_develops)
             co_build_size = tree.xpath('//span[@id="cph_hif1_jzmj"]/text()')[0]  # 建筑面积
             # print(co_build_size)
             co_green = tree.xpath('//span[@id="cph_hif1_lhl"]/text()')[0]  # 绿化率
             if not co_green:
                 return
             # print(co_green)
             co_volumetric = tree.xpath('//span[@id="cph_hif1_rjl"]/text()')[0]  # 容积率
             # print(co_volumetric)
             co_all_house = tree.xpath('//span[@id="cph_hif1_fwts"]/text()')[0]  # 小区总套数
             # print(co_all_house)
             co_open_time = tree.xpath('//span[@id="cph_hif1_kpsj"]/font/text()')[0]  # 小区开盘时间
             # print(co_open_time)
             co_handed_time = tree.xpath('//span[@id="cph_hif1_jfsj"]/font/text()')[0]  # 小区交房时间
             # print(co_handed_time)
             # comm.co_name = co_name
             # comm.co_pre_sale = co_pre_sale
             # comm.co_address = co_address
             # comm.co_develops = co_develops
             # comm.co_build_size = co_build_size
             # comm.co_green = co_green
             # comm.co_volumetric = co_volumetric
             # comm.co_all_house = co_all_house
             # comm.co_open_time = co_open_time
             # comm.co_handed_time = co_handed_time
             # 获取楼栋url
             build_url = tree.xpath('//a[@id="hdl1_hlink3"]/@href')[0]
             building = Building()
             build_obj = self.get_build_detail(build_url, building)
             # build_obj.insert_db()
        except Exception as e:
            print('retry')
            raise


    @retry(retry(3))
    def get_build_detail(self, build_url):
        res = requests.get(url=build_url)
        html = res.content.decode()
        tree = etree.HTML(html)
        # 获取楼栋信息
        build_content = tree.xpath('//table[@id="cph_hb1_dg1"]/tbody/tr[position()>1]')
        for i in build_content:
            bu_num = build_content.xpath('td[1]/text')[0]
            bu_all_house = build_content.xpath('td[3]/text')[0]
            building.bu_num = bu_num
            building.bu_all_house = bu_all_house
            # building_data =
            ho_url = build_content.xpath('td[7]/font/a/@href')
            house = House()
            house_obj = self.get_house_detail(ho_url)


    # def get_house_d etail(self, ho_url):




if __name__ == '__main__':
    b = Bijie()
    b.start_crawler()

