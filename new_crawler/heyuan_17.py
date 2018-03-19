"""
网站防火墙
"""
"""
url = http://183.63.60.194:8808/public/web/index
city : 河源
CO_INDEX : 17
author:
小区数量：
"""

from comm_info import Comm, Building, House
import re, requests

url = 'http://183.63.60.194:8808/public/web/index?jgid=FC830662-EA75-427C-9A82-443B91E383CB'
co_index = '17'
city = '河源'


class Heyuan(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
        }

    def start_crawler(self):
        info_url = 'http://183.63.60.194:8808/api/GzymApi/GetIndexSearchData?Jgid=FC830662-EA75-427C-9A82-443B91E383CB&PageIndex=1&PageSize=2000&Ysxmmc=&Ysxkzh=&Kfsmc=&Kfxmmc='
        response = requests.get(info_url, headers=self.headers)
        html = response.text
        if '网站防火墙' in html:
            print('\r\n\r\n             网站防火墙\r\n\r\n')
            return
        co_url_list = re.findall('YSXMID":"(.*?)"', html)
        self.get_comm_info(co_url_list)

    def get_comm_info(self, co_url_list):
        for i in co_url_list:
            try:
                comm = Comm(co_index)
                comm_url = 'http://183.63.60.194:8808/public/web/ysxm?ysxmid=' + i
                response = requests.get(comm_url, headers=self.headers)
                html = response.text
                comm.co_develops = re.findall('kfsmc.*?<a.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_name = re.findall('PresellName.*?<a.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_address = re.findall('ItemRepose.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_build_size = re.findall('PresellArea.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_all_house = re.findall('djrqtd.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_land_use = re.findall('landinfo.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_type = re.findall('zczjtd.*?>(.*?)<', html, re.S | re.M)[0]
                comm.area = re.findall('FQ.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_pre_sale_date = re.findall('FZDatebegin.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_pre_sale = re.findall('bookid.*?<a.*?>(.*?)<', html, re.S | re.M)[0]
                comm.insert_db()
                bu_address_list = re.findall('onmouseout.*?center.*?center">(.*?)<', html, re.S | re.M)
                bu_num_list = re.findall('onmouseout.*?center.*?center.*?center">(.*?)<', html, re.S | re.M)
                bu_floor_list = re.findall('onmouseout.*?center.*?center.*?center.*?center">(.*?)<', html, re.S | re.M)
                bu_url_list = re.findall('onmouseout.*?href="(.*?)"', html, re.S | re.M)
                self.get_build_info(bu_address_list, bu_num_list, bu_floor_list, bu_url_list, comm.co_name)
            except Exception as e:
                print(e)

    def get_build_info(self, bu_address_list, bu_num_list, bu_floor_list, bu_url_list, co_name):
        for i in range(len(bu_url_list)):
            build = Building(co_index)
            build.bu_address = bu_address_list[i]
            build.bu_num = bu_num_list[i]
            build.bu_floor = bu_floor_list[i]
            build.co_name = co_name
            build.insert_db()
            response = requests.get('http://183.63.60.194:8808/public/web/lpb?' + bu_url_list[i], headers=self.headers)
            html = response.text
            house_url_list = re.findall('房屋号：<a.*?href="(.*?)"', html, re.S | re.M)
            self.get_house_info(house_url_list)

    def get_house_info(self, house_url_list):
        for i in house_url_list:
            house_url = 'http://183.63.60.194:8808/public/web/' + i
            response = requests.get(house_url, headers=self.headers)
            if response.status_code is not 200:
                continue
            html = response.text
            bu_num_list = re.findall('DongNo.*?>(.*?)<', html, re.S | re.M)
            ho_name_list = re.findall('HouseNO.*?>(.*?)<', html, re.S | re.M)
            ho_true_size_list = re.findall('HouseArea.*?>(.*?)<', html, re.S | re.M)
            ho_build_size_list = re.findall('SumBuildArea1.*?>(.*?)<', html, re.S | re.M)
            ho_type_list = re.findall('HouseUse.*?>(.*?)<', html, re.S | re.M)
            orientation_list = re.findall('CHX.*?>(.*?)<', html, re.S | re.M)
            for index in range(len(bu_num_list)):
                house = House(co_index)
                house.bu_num = bu_num_list[index]
                house.ho_name = ho_name_list[index]
                house.ho_true_size = ho_true_size_list[index]
                house.ho_build_size = ho_build_size_list[index]
                house.ho_type = ho_type_list[index]
                house.orientation = orientation_list[index]
                house.insert_db()


if __name__ == '__main__':
    h = Heyuan()
    h.start_crawler()
