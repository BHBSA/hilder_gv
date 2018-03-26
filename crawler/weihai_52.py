"""
url = http://221.2.144.162:8090/loupan_list.asp
city : 威海
CO_INDEX : 52
小区数量：
对应关系：
"""

import requests
from comm_info import Comm, Building, House
import re

url = 'http://221.2.144.162:8090/loupan_list.asp?area=&name='
co_index = '52'
city = '威海'


class Weihai(object):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
        }

    def start_crawler(self):
        for i in range(1, 47):
            try:
                index_url = 'http://221.2.144.162:8090/loupan_list.asp?Page=' + str(i)
                response = requests.get(index_url, headers=self.headers)
                html = response.content.decode('gbk')
                comm_url_list = re.findall('\[项目网站\] \[<a href=(.*?) target', html, re.S | re.M)
                self.get_comm_info(comm_url_list)
            except Exception as e:
                print(e)

    def get_comm_info(self, comm_url_list):
        for i in comm_url_list:
            try:
                comm = Comm(co_index)
                comm_url = 'http://221.2.144.162:8090/' + i
                response = requests.get(comm_url, headers=self.headers)
                html = response.content.decode('gbk')
                comm.co_name = re.findall('项目名称：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_develops = re.findall('开 发 商：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                comm.area = re.findall('城 &nbsp;&nbsp;&nbsp;区：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_type = re.findall('物业类型：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_address = re.findall('物业位置：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                comm.co_build_size = re.findall('建筑面积：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                comm.insert_db()
                build_url_list = re.findall("height=20.*?<a href=(.*?) ", html, re.S | re.M)
                bu_pre_sale_list = re.findall("height=20.*?<Td>(.*?)<", html, re.S | re.M)
                self.get_build_info(build_url_list, bu_pre_sale_list, comm.co_name)
            except Exception as e:
                print(e)

    def get_build_info(self, build_url_list, bu_pre_sale_list, co_name):
        for i in range(len(build_url_list)):
            try:
                build = Building(co_index)
                build.co_name = co_name
                build.bu_pre_sale = bu_pre_sale_list[i]
                build_url = 'http://221.2.144.162:8090/' + build_url_list[i]
                response = requests.get(build_url, headers=self.headers)
                html = response.content.decode('gbk')
                build.bu_num = re.findall('<font color=white.*?><b>(.*?)<', html, re.S | re.M)[0]
                build.bu_address = re.findall('坐落位置：</b>(.*?)<', html, re.S | re.M)[0]
                build.insert_db()
                ho_name_list = re.findall('background-.*?href=.*?>(.*?)<', html, re.S | re.M)
                for i in ho_name_list:
                    try:
                        house = House(co_index)
                        house.bu_num = build.bu_num
                        house.co_name = co_name
                        house.ho_name = i
                        house.insert_db()
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
