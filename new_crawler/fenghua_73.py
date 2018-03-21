"""
url = http://old.newhouse.cnnbfdc.com/lpxx.aspx
city : 奉化
CO_INDEX : 73
小区数量：
对应关系：
    小区与楼栋：
    楼栋与房屋：
"""
import requests
from lxml import etree
from producer import ProducerListUrl
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
import re

url = 'http://old.newhouse.cnnbfdc.com/lpxx.aspx'
co_index = '73'
city = '奉化'


class Fenghua(object):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
        }

    def start_crawler(self):
        res = requests.get(url, headers=self.headers)
        html = res.text
        page = re.search('>><.*?p=(.*?)"', html, re.S | re.M).group(1)
        for i in range(1, int(page) + 1):
            page_url = 'http://old.newhouse.cnnbfdc.com/lpxx.aspx?p=' + str(i)
            response = requests.get(page_url, headers=self.headers)
            content = response.text
            comm_url_list = re.findall('align="left" bgcolor="#FFFFFF".*?href="(.*?)"', content, re.S | re.M)
            self.get_comm_info(comm_url_list)

    def get_comm_info(self, comm_url_list):
        for i in comm_url_list:
            comm = Comm(co_index)
            comm_url = 'http://old.newhouse.cnnbfdc.com/' + i
            response = requests.get(comm_url, headers=self.headers)
            html = response.text
            comm.co_name = re.findall('项目名称：.*?<span.*?>(.*?)<', html, re.S | re.M)[0]
            comm.co_address = re.findall('项目地址：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
            comm.co_develops = re.findall('开发公司：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
            comm.co_pre_sale = re.findall('售证名称：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
            comm.co_build_size = re.findall('纳入网上可售面积：.*?<img.*?>(.*?)<', html, re.S | re.M)[0]
            comm.co_all_house = re.findall('纳入网上可售套数：.*?<img.*?>(.*?)<', html, re.S | re.M)[0]
            comm.area = re.findall('所在区县：.*?<td.*?>(.*?)<', html, re.S | re.M)[0]
            bu_all_house_list = re.findall('window.open.*?center.*?center.*?>(.*?)<', html, re.S | re.M)
            bu_url_list = re.findall("window\.open\('(.*?)'", html, re.S | re.M)
            for i in range(len(bu_url_list)):
                build = Building(co_index)
                bu_url = bu_url_list[i]
                build.bu_all_house = bu_all_house_list[i]
                build.co_name = comm.co_name
                build.insert_db()
                self.get_house_info(bu_url)

    def get_house_info(self, bu_url):
        qrykey = re.search('qrykey=(.*?)&', bu_url).group(1)
        house_url = 'http://old.newhouse.cnnbfdc.com/GetHouseTable.aspx?qrykey=' + qrykey
        response = requests.get(house_url, headers=self.headers)
        html = response.text
        house_code_list = re.findall("onclick=select_room\('(.*?)'", html, re.S | re.M)
        for i in house_code_list:
            house_detail_url = 'http://old.newhouse.cnnbfdc.com/openRoomData.aspx?roomId='+str(i)
            res = requests.get(house_detail_url,headers=self.headers)
            content = res.text
            re.findall('')

