"""
url = http://www.fzfgj.cn/website/search/q.html?type=spf&page=1
city : 抚州
CO_INDEX : 11
author: 吕三利
小区数量：14页    2018/2/27
"""

from base import AllListUrl
from crawler_base import Crawler
from lxml import etree
from comm_info import Comm, Building, House
import requests, re
from retry import retry

CO_INDEX = 11


class Fuzhou(Crawler):
    def __init__(self):
        self.url = 'http://www.fzfgj.cn/website/search/q.html?type=spf&page=1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        }

    def start_crawler(self):
        self.start()

    @retry(retry(3))
    def start(self):
        b = AllListUrl(first_page_url=self.url,
                       request_method='get',
                       encode='gbk',
                       regex_group=1,
                       regex='共(.*?)页', )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            response = requests.get(url=self.url, headers=self.headers)
            html = response.text
            tree = etree.HTML(html)
            comm_url_list = tree.xpath('//*[@id="houseList0"]/dt/a/@href')
            for i in comm_url_list:
                comm = Comm()
                url = 'http://www.fzfgj.cn/' + i
                self.get_comm_info(url, comm)

    @retry(retry(3))
    def get_comm_info(self, url, comm):
        try:
            response = requests.get(url=url, headers=self.headers)
            html = response.text
            tree = etree.HTML(html)
            # 小区名称
            co_name = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox3"]/div/table/tr[1]/td[2]/text()')[0].strip()
            # 小区地址
            co_address = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox3"]/div/table/tr[2]/td[2]/text()')[0].strip()
            # 开工时间
            co_build_start_time = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox3"]/div/table/tr[3]/td[2]/text()')[
                0].strip()
            # 竣工时间
            co_build_end_time = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox3"]/div/table/tr[3]/td[4]/text()')[0].strip()
            # 建筑结构
            co_build_structural = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox3"]/div/table/tr[4]/td[2]/text()')[
                0].strip()
            # 容积率
            co_volumetric = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox3"]/div/table/tr[6]/td[4]/text()')[0].strip()
            # 绿化率
            co_green = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox3"]/div/table/tr[6]/td[2]/text()')[0].strip()
            # 占地面的
            co_size = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox3"]/div/table/tr[5]/td[2]/text()')[0].strip()
            co_id = re.search('home/(.*?).html', url).group(1)
            comm.co_index = CO_INDEX
            comm.co_name = co_name
            comm.co_address = co_address
            comm.co_build_start_time = co_build_start_time
            comm.co_build_end_time = co_build_end_time
            comm.co_build_structural = co_build_structural
            comm.co_volumetric = co_volumetric
            comm.co_green = co_green
            comm.co_size = co_size
            comm.co_id = co_id
            build_info_list = tree.xpath('//*[@id="ctl00_CPH_M_sm_spfBox1"]/div/table/tr[@class="hobuild"]')
            for i in build_info_list:
                build = Building()
                # 楼栋名称
                bu_name = i.xpath('string(td[1])')
                # 楼栋id
                bu_id = i.xpath('td[1]/strong/a/@href')[0]
                bu_id = re.search('building_id=(.*?)$', bu_id).group(1)
                # 建筑面积
                bu_build_size = i.xpath('string(td[3])').replace('�O', '')
                self.get_build_info(bu_id, co_id)
                build.co_index = CO_INDEX
                build.co_id = co_id
                build.bu_id = bu_id
                build.bu_name = bu_name
                build.bu_build_size = bu_build_size
                build.insert_db()
            comm.insert_db()
        except BaseException as e:
            print(e)


    @retry(retry(3))
    def get_build_info(self, bu_id, co_id):
        try:
            url = 'http://www.fzfgj.cn/website/presale/home/HouseTableControl/GetData.aspx?Building_ID=' + bu_id
            response = requests.get(url=url, headers=self.headers)
            xml = response.text
            tree = etree.XML(xml)
            logo = tree.xpath('//LOGICBUILDING_ID/text()')[0]
            url_2 = 'http://www.fzfgj.cn/website/presale/home/HouseTableControl/GetData.aspx?LogicBuilding_ID=' + logo
            result = requests.get(url_2)
            xml_2 = result.text
            tree_2 = etree.XML(xml_2)
            house_info_list = tree_2.xpath('T_HOUSE')
            for i in house_info_list:
                house = House()
                ho_num = i.xpath('//HOUSE_NUMBER/text()')[0]
                ho_name = i.xpath('//ROOM_NUMBER/text()')[0]
                ho_build_size = i.xpath('//BUILD_AREA/text()')[0]
                ho_true_size = i.xpath('//BUILD_AREA_INSIDE/text()')[0]
                ho_share_size = i.xpath('//BUILD_AREA_SHARE/text()')[0]
                ho_floor = i.xpath('//FLOOR_REALRIGHT/text()')[0]
                ho_type = i.xpath('//USE_FACT/text()')[0]
                house.co_index = CO_INDEX
                house.co_id = co_id
                house.bu_id = bu_id
                house.ho_build_size = ho_build_size
                house.ho_true_size = ho_true_size
                house.ho_share_size = ho_share_size
                house.ho_floor = ho_floor
                house.ho_num = ho_num
                house.ho_name = ho_name
                house.ho_type = ho_type
                house.insert_db()
        except BaseException as e:
            print(e)

