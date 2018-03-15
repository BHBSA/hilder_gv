"""
url = http://old.newhouse.cnnbfdc.com/lpxx.aspx
city : 宁波
CO_INDEX : 33
小区数量：
对应关系：
"""

import requests
from lxml import etree
from producer import ProducerListUrl
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from retry import retry
import re

url = 'http://old.newhouse.cnnbfdc.com/lpxx.aspx'
co_index = '33'
city = '宁波'


class Ningbo(object):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
        }

    def start_crawler(self):
        b = AllListUrl(first_page_url=url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='utf-8',
                       page_count_rule='>><.*?aspx\?p=(.*?)"',
                       headers=self.headers
                       )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            all_page_url = url + '?p=' + str(i)
            response = requests.get(all_page_url, headers=self.headers)
            html = response.text
            tree = etree.HTML(html)
            comm_url_list = tree.xpath('//a[@class="sp_zi12c"]/@href')
            self.get_comm_info(comm_url_list)

    @retry(tries=3)
    def get_comm_info(self, comm_url_list):
        for i in comm_url_list:
            try:
                comm = Comm(co_index)
                comm_url = 'http://old.newhouse.cnnbfdc.com/' + i
                response = requests.get(comm_url, headers=self.headers)
                html = response.text
                comm.co_name = re.findall('项目名称：.*?<span.*?>(.*?)<', html, re.S | re.M)[0].strip()
                comm.co_address = re.findall('项目地址：.*?<td.*?>(.*?)<', html, re.S | re.M)[0].strip()
                comm.co_develops = re.findall('开发公司：.*?<td.*?>(.*?)<', html, re.S | re.M)[0].strip()
                comm.co_pre_sale = re.findall('预\(现\)售证名称：.*?<td.*?>(.*?)<', html, re.S | re.M)[0].strip()
                comm.co_build_size = re.findall('纳入网上可售面积：.*?<img.*?>(.*?)<', html, re.S | re.M)[0].strip()
                comm.co_all_house = re.findall('纳入网上可售套数：.*?<img.*?>(.*?)<', html, re.S | re.M)[0].strip()
                comm.area = re.findall('所在区县：.*?<td.*?>(.*?)<', html, re.S | re.M)[0].strip()
                comm.co_id = re.findall('mobanshow.aspx\?projectid=(.*?)"', html, re.S | re.M)[0].strip()
                comm.insert_db()
                build_url_list = re.findall("window.open\('(.*?)'", html, re.S | re.M)
                bu_name_list = re.findall("window.open.*?<font.*?>(.*?)<", html, re.S | re.M)
                bu_all_house_list = re.findall("window.open.*?<td.*?>(.*?)<", html, re.S | re.M)
                qrykey = re.findall("qrykey=(.*?)&", html, re.S | re.M)
                for index in range(len(build_url_list)):
                    build = Building(co_index)
                    build.bu_name = bu_name_list[index].strip()
                    build.bu_all_house = bu_all_house_list[index].strip()
                    build.co_id = comm.co_id.strip()
                    build.bu_id = qrykey[index].strip()
                    build.insert_db()
                self.get_house_info(build_url_list)
            except BaseException as e:
                print(e)

    @retry(tries=3)
    def get_house_info(self, build_url_list):
        for i in build_url_list:
            try:
                qrykey = re.search('qrykey=(.*?)&', i).group(1)
                house_url = 'http://old.newhouse.cnnbfdc.com/GetHouseTable.aspx?qrykey=' + qrykey
                response = requests.get(house_url, headers=self.headers)
                html = response.text
                # house_info_url_list = re.findall('javascript:window.open\("(.*?)"', html, re.S | re.M)
                info_list = re.findall('(房号：.*?")', html, re.S | re.M)
                ho_name_list = re.findall('title=.*?center.*?center.*?<a.*?>(.*?)<', html, re.S | re.M)
                for index in range(len(info_list)):
                    house = House(co_index)
                    house.info = info_list[index]
                    house.ho_name = ho_name_list[index]
                    house.bu_id = qrykey
                    house.insert_db()
                    # 房屋详情页面
                    # self.get_house_detail(house_info_url_list, qrykey)
            except BaseException as e:
                print(e)
                # 房屋页面响应太慢
                # @retry(tries=3)
                # def get_house_detail(self, house_info_url_list, qrykey):
                #     for i in house_info_url_list:
                #         try:
                #             house = House(co_index)
                #             house_url = 'http://old.newhouse.cnnbfdc.com/' + i
                #             response = requests.get(house_url, headers=self.headers)
                #             html = response.text
                #             house.ho_name = re.findall('户室名称（室号）.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                #             house.ho_floor = re.findall('实际楼层.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                #             house.ho_room_type = re.findall('户型.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                #             house.ho_type = re.findall('房屋用途.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                #             house.ho_build_size = re.findall('预测建筑面积.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                #             house.ho_true_size = re.findall('预测套内面积.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                #             house.ho_share_size = re.findall('预测分摊面积.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
                #             house.bu_id = qrykey
                #             house.insert_db()
                #         except BaseException as e:
                #             print(e)
