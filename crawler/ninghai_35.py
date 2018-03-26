"""
url = http://www.nhfg.cn/webhouseinfo/ItemSearch/ItemSearch.aspx
city : 宁海
CO_INDEX : 35
小区数量：
对应关系：小区与楼栋：co_id
        楼栋与房号：bu_num
"""

import requests
from comm_info import Comm, Building, House
from lxml import etree
import re
from urllib import parse

url = 'http://www.nhfg.cn/webhouseinfo/ItemSearch/ItemSearch.aspx'
co_index = '35'
city = '宁海'


class Ninghai(object):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
        }

    def start_crawler(self):
        all_comm_url_dict = {
            'area_list': [],
            'comm_url_list': []
        }
        response = requests.get(url=url)
        html = response.text
        comm_url_list = re.findall("</font></td><td align=.center. width=.100.><font color=.#000066.>.*?href='(.*?)'",
                                   html, re.S | re.M)
        area_list = re.findall("</tr><tr>.*?<td.*?href='../ItemList.*?<font.*?>(.*?)<", html, re.S | re.M)
        for i in range(len(comm_url_list)):
            all_comm_url_dict['area_list'].append(area_list[i])
            all_comm_url_dict['comm_url_list'].append(comm_url_list[i])
        data = self.get_view_state(html)
        comm_dict = self.get_all_url_comm(data, 0, all_comm_url_dict)
        comm_url_list = comm_dict['comm_url_list']
        area_list = comm_dict['area_list']
        for i in range(len(comm_url_list)):
            comm_url = 'http://www.nhfg.cn/webhouseinfo' + comm_url_list[i]
            area = area_list[i]
            self.get_comm_info(comm_url, area)

    def get_comm_info(self, comm_url, area):
        try:
            comm = Comm(co_index)
            comm.area = area.strip()
            comm_url = comm_url.replace('..', '')
            response = requests.get(comm_url)
            html = response.text
            comm.co_name = re.findall('项目名称：.*?<TD.*?><FONT.*?>(.*?)<', html, re.S | re.M)[0].strip()
            comm.co_address = re.findall('项目地址：.*?<TD.*?>(.*?)<', html, re.S | re.M)[0].strip()
            comm.co_develops = re.findall('开发公司：.*?<TD.*?>(.*?)<', html, re.S | re.M)[0].strip()
            comm.co_pre_sale = re.findall('预售证名称：.*?<TD.*?>(.*?)<', html, re.S | re.M)[0].strip()
            comm.co_build_size = re.findall('纳入网上可售面积：.*?<TD.*?>(.*?)<', html, re.S | re.M)[0].strip()
            comm.co_id = re.search('\?(.*?)$', comm_url).group(1)
            comm.insert_db()
            build_url_list = re.findall("(HouseList/HouseInfo.aspx\?.*?)'", html, re.S | re.M)
            self.get_build_url(build_url_list, comm.co_id)
        except Exception as e:
            print(e)

    def get_build_url(self, build_url_list, co_id):
        for i in build_url_list:
            try:
                build = Building(co_index)
                build.co_id = co_id
                bu_url = 'http://www.nhfg.cn/webhouseinfo/ItemList/' + i
                response = requests.get(bu_url)
                html = response.text
                build.bu_num = \
                    re.findall('<TD style="WIDTH: 471px" colSpan="11"><FONT style="COLOR: white" face="宋体">(.*?)<',
                               html,
                               re.S | re.M)[0].strip()
                build.bu_all_house = re.findall('商业</FONT></TD>.*?center">(.*?)<', html, re.S | re.M)[0].strip()
                build.insert_db()
                house_url = re.findall('(RoomLoad\.aspx\?.*?)"', html, re.S | re.M)[0]
                zu_house_url = 'http://www.nhfg.cn/webhouseinfo/ItemList/HouseList/' + house_url
                self.get_house_info(zu_house_url, build.bu_num, co_id)
            except Exception as e:
                print(e)

    def get_house_info(self, zu_house_url, bu_num, co_id):
        try:
            house = House(co_index)
            house.bu_num = bu_num
            house.co_id = co_id
            result = requests.get(zu_house_url, headers=self.headers).text
            house.info = re.search('ItemName.*?>(.*?)<', result).group(1).strip()
            ho_name_list = re.findall("OnClick=.__doPostBack\(.*?,'(.*?)'\)", result, re.S | re.M)
            view_ = re.search('id="__VIEWSTATE.*?value="(.*?)" />', result, re.S | re.M).group(1)
            self.get_house_detail(ho_name_list, view_)
        except Exception as e:
            print(e)

    def get_house_detail(self, ho_name_list, view_):
        for i in ho_name_list:
            # s = requests.session()
            code = i.replace('amp;', '')

            data = {
                '__VIEWSTATE': view_,
                '__VIEWSTATEGENERATOR': 'C5D03DD7',
                '__EVENTTARGET': 'WebChessTabForSqlCtl1',
                '__EVENTARGUMENT': parse.quote(code,encoding='utf8'),
                'WebChessTabForSqlCtl1': None
            }
            result = requests.post('http://www.nhfg.cn/webhouseinfo/ItemList/HouseList/RoomLoad.aspx?153', data=data,
                            headers=self.headers)
            s_id = result.cookies.get_dict()['NHREMO_SessionId']
            data2 = {
                'Cookie': 'NHREMO_SessionId=' + s_id,
            }
            response = requests.get('http://www.nhfg.cn/webhouseinfo/ItemList/HouseList/RoomInfo.aspx',
                                    headers=data2)
            html = response.content.decode('gb2312')

    def get_view_state(self, html):
        tree = etree.HTML(html)
        view_state = tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
        event_validation = tree.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
        data = {
            '__EVENTTARGET': 'lnkbtnNext',
            '__EVENTVALIDATION': event_validation,
            '__VIEWSTATE': view_state,
        }
        return data

    def get_all_url_comm(self, data, index, all_comm_url_dict):
        response = requests.post(url=url, data=data)
        html = response.text
        comm_url_list = re.findall("</font></td><td align=.center. width=.100.><font color=.#000066.>.*?href='(.*?)'",
                                   html, re.S | re.M)
        area_list = re.findall("</tr><tr>.*?<td.*?href='../ItemList.*?<font.*?>(.*?)<", html, re.S | re.M)
        for i in range(len(comm_url_list)):
            all_comm_url_dict['area_list'].append(area_list[i])
            all_comm_url_dict['comm_url_list'].append(comm_url_list[i])
        data = self.get_view_state(html)
        index += 1
        print(index)
        if index == 2:
            return all_comm_url_dict
        else:
            return self.get_all_url_comm(data, index, all_comm_url_dict)
