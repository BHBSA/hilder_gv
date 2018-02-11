"""
url: http://61.178.148.157:8081/bit-xxzs/xmlpzs/nowwebissue.asp
city: 白银
CO_INDEX: 0
author: 吕三利
小区个数：54962   2018/2/11
"""
CO_INDEX = 0
import requests
from lxml import etree
import re
from comm_info import Comm, Building
from crawler_base import Crawler
from retry import retry


class Baiyin(Crawler):
    url = 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/nowwebissue.asp'

    @retry(tries=3)
    def get_all_page(self):
        try:
            res = requests.get(url=self.url)
            html = res.content.decode('gbk').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
            page = re.search(r'共有(.*?)页', html).group(1)
            print(page)
            return page
        except Exception as e:
            print(e)
            raise

    @retry(tries=3)
    def baiyin_start(self):
        page = self.get_all_page()
        for i in range(1, int(page) + 1):
            res = requests.get(self.url + '?page=' + str(i))
            html = res.content.decode('gbk')
            tree = etree.HTML(html)
            community_list = tree.xpath('//tr[@align="center"]')
            for i in community_list:
                try:
                    comm = Comm()
                    href = i.xpath('td/a/@href')
                    if not href:
                        continue
                    href = href[0]
                    self.get_comm_detail(href, comm)
                except Exception as e:
                    href = i.xpath('td/a/@href')
                    if not href:
                        continue
                    href = href[0]
                    comm_url = 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/' + href
                    print('小区错误：', comm_url)

    @retry(tries=3)
    def get_comm_detail(self, href, comm):
        comm_detail_url = 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/' + href
        response = requests.get(url=comm_detail_url)
        co_id = response.url
        co_id = int(co_id.split('=')[1])  # 小区id
        html = response.content.decode('gbk').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
        co_name = re.search(r'项目名称(.*?)<td>(.*?)</td>', html).group(2)  # 小区名字
        co_owner = re.search(r'房屋所有权证号(.*?)<td>(.*?)</td>', html).group(2)
        certificate = re.search(r'房屋所有权证号(.*?)<td>(.*?)</td>', html).group(2)
        approve_Times = re.search(r'批准时间(.*?)<td>(.*?)</td>', html).group(2)
        use = re.search(r'用　　途(.*?)<td>(.*?)</td>', html).group(2)
        co_type = re.search(r'项目类型(.*?)<td>(.*?)</td>', html).group(2)  # 小区类型
        co_size = re.search(r'批准面积(.*?)<td>(.*?)</td>', html).group(2)  # 占地面积
        comm.co_id = co_id
        comm.co_name = co_name
        comm.co_type = co_type
        comm.co_size = co_size
        comm.co_index = CO_INDEX
        comm.co_owner = co_owner
        # 获取楼栋url列表
        build_url_list = re.findall(r"<td><ahref='(.*?)'", html)
        if not build_url_list:
            return
        else:
            for build_url in build_url_list:
                try:
                    building = Building()
                    build_id = re.search(r'<td>(\d{2,6})</td>', html).group(1)  # 楼栋id
                    bu_all_house = re.search(r'<td>(\d{1,3})</td>', html).group(1)  # 总套数
                    house_url = re.search(r'<td><ahref="(.*?)"', html).group(1)
                    bu_price_demo = re.findall('<td>[\.\d]+</td>', html)[4]
                    bu_price = re.search('\d+', bu_price_demo).group()
                    data_dict = self.get_build_detail(build_url)
                    bu_num = data_dict['bu_num']  # 楼号
                    bu_build_size = data_dict['bu_build_size']  # 建筑面积
                    co_address = data_dict['co_address']  # 小区地址
                    co_build_end_time = data_dict['co_build_end_time']  # 竣工时间
                    co_build_type = data_dict['co_build_type']  # 竣工时间
                    if not co_build_end_time:
                        building.co_is_build = '1'
                    bu_floor = self.get_house_detail(house_url)
                    # 小区
                    comm.co_address = co_address
                    comm.co_build_end_time = co_build_end_time
                    comm.bu_build_size = bu_build_size
                    comm.co_build_type = co_build_type
                    # 楼栋
                    building.bu_num = bu_num
                    building.bu_build_size = bu_build_size
                    building.bu_floor = bu_floor
                    building.bu_all_house = bu_all_house
                    building.bu_id = build_id
                    building.co_id = co_id
                    building.co_index = CO_INDEX
                    building.bu_price = bu_price
                    # 插入
                    building.insert_db()
                except Exception as e:
                    build_detail_url = 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/' + build_url
                    print('楼栋错误：', build_detail_url)
        comm.insert_db()

    @retry(tries=3)
    def get_build_detail(self, build_url):
        build_detail_url = 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/' + build_url
        response = requests.get(url=build_detail_url)
        html = response.content.decode('gbk').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
        bu_num = re.search('销售楼号(.*?)<td>(.*?)</td>', html).group(2)  # 楼号
        bu_build_size = re.search('建筑面积(.*?)<td>(.*?)</td>', html).group(2)  # 建筑面积
        co_address = re.search('楼盘座落(.*?)<td>(.*?)</td>', html).group(2)  # 小区地址
        co_build_end_time = re.search('完工日期(.*?)<td>(.*?)</td>', html).group(2)  # 竣工时间
        co_build_type = re.search('楼盘结构(.*?)<td>(.*?)</td>', html).group(2)  # 建筑结构
        data_dict = {}
        data_dict['bu_num'] = bu_num
        data_dict['bu_build_size'] = bu_build_size
        data_dict['co_address'] = co_address
        data_dict['co_build_end_time'] = co_build_end_time
        data_dict['co_build_type'] = co_build_type
        return data_dict

    @retry(tries=3)
    def get_house_detail(self, href):
        url = 'http://61.178.148.157:8081' + href
        response = requests.get(url)
        html = response.content.decode('gbk').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
        bu_floor = re.search(r'(\d)\[\d+套/([\d\.]+)平方米', html).group(1)
        return bu_floor

    def start_crawler(self):
        self.baiyin_start()


if __name__ == '__main__':
    b = Baiyin()
    b.baiyin_start()
