"""
url = http://www.funi.com/loupan/region_0_0_0_0_1
city: 成都
CO_INDEX: 5
author: 吕三利
小区数量：3376   2018/2/22
"""

from crawler_base import Crawler
from lxml import etree
from comm_info import Comm
import requests
from retry import retry



class Chengdu(Crawler):
    def __init__(self):
        self.url = 'http://www.funi.com/loupan/region_0_0_0_0_1'
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        }

    def start_crawler(self):
        self.start()

    def get_all_page(self):
        response = requests.get(url=self.url,headers=self.headers)
        html = response.text
        tree = etree.HTML(html)
        page = tree.xpath('//div[@class="pages"]/a/text()')[-2]
        print(page)
        return page

    @retry(retry(3))
    def start(self):
        page = self.get_all_page()
        for i in range(1, int(page) + 1):
            url = 'http://www.funi.com/loupan/region_0_0_0_0_' + str(i)
            response = requests.get(url,headers=self.headers)
            html = response.text
            tree = etree.HTML(html)
            comm_url_list = tree.xpath('//dt[@class="clearfix"]/h2/a/@href')
            for i in comm_url_list:
                comm = Comm(5)
                i = i.split(';')
                if i:
                    i = i[0]
                url = 'http://www.funi.com/' + i + '/detail.htm'
                try:
                    self.get_comm_detail(url, comm)
                except Exception as e:
                    print('小区错误：', url)

    @retry(retry(3))
    def get_comm_detail(self, url, comm):
        try:
            response = requests.get(url,headers=self.headers)
            html = response.text
            tree = etree.HTML(html)
            co_name = tree.xpath('//div[@class="info"]/h1/text()')[0].strip()  # 小区名字
            co_build_size = tree.xpath('//div[@class="intro"]/dl[1]/dd/ul/li[1]/em/i/text()')  # 建筑面积
            if co_build_size:
                co_build_size = co_build_size[0].replace('㎡', '').strip()
            else:
                co_build_size = None
            co_size = tree.xpath('//div[@class="intro"]/dl[1]/dd/ul/li[2]/em/i/text()')  # 占地面的
            if co_size:
                co_size = co_size[0].replace('㎡', '').strip()
            else:
                co_size = None
            co_volumetric = tree.xpath('//div[@class="intro"]/dl[1]/dd/ul/li[3]/em/i/text()')  # 容积率
            if co_volumetric:
                co_volumetric = co_volumetric[0]
            else:
                co_volumetric = None
            co_green = tree.xpath('//div[@class="intro"]/dl[1]/dd/ul/li[4]/em/i/text()')  # 绿化率
            if co_green:
                co_green = co_green[0]
            else:
                co_green = None
            co_address = tree.xpath('//div[@class="intro"]/dl[1]/dd/ul/li[6]/em/i/text()')  # 小区地址
            if co_address:
                co_address = co_address[0]
            else:
                co_address = None
            co_develops = tree.xpath('//div[@class="intro"]/dl[1]/dd/ul/li[8]/em/text()')  # 开发商
            if co_develops:
                co_develops = co_develops[0]
            else:
                co_develops = None
            co_pre_sale = tree.xpath('//div[@class="intro"]/dl[1]/dd/ul/li[9]/em/text()')  # 预售证书
            if co_pre_sale:
                co_pre_sale = co_pre_sale[0]
            else:
                co_pre_sale = None
            co_type = tree.xpath('//div[@class="intro"]/dl[2]/dd/ul/li[1]/em/text()')  # 小区类型
            if co_type:
                co_type = co_type[0]
            else:
                co_type = None
            co_build_type = tree.xpath('//div[@class="intro"]/dl[2]/dd/ul/li[2]/em/text()')  # 建筑类型
            if co_build_type:
                co_build_type = co_build_type[0]
            else:
                co_build_type = None
            co_open_time = tree.xpath('//div[@class="intro"]/dl[2]/dd/ul/li[11]/em/text()')  # 小区开盘时间
            if co_open_time:
                co_open_time = co_open_time[0]
            else:
                co_open_time = None
            co_handed_time = tree.xpath('//div[@class="intro"]/dl[2]/dd/ul/li[12]/em/text()')  # 小区交房时间
            if co_handed_time:
                co_handed_time = co_handed_time[0]
            else:
                co_handed_time = None
            co_all_house = tree.xpath('//div[@class="intro"]/dl[2]/dd/ul/li[5]/em/text()')  # 小区总套数
            if co_all_house:
                co_all_house = co_all_house[0]
            else:
                co_all_house = None
            comm.co_name = co_name
            comm.co_address = co_address
            comm.co_type = co_type
            comm.co_build_type = co_build_type
            comm.co_green = co_green
            comm.co_size = co_size
            comm.co_build_size = co_build_size
            comm.co_develops = co_develops
            comm.co_pre_sale = co_pre_sale
            comm.co_open_time = co_open_time
            comm.co_handed_time = co_handed_time
            comm.co_all_house = co_all_house
            comm.co_volumetric = co_volumetric
            comm.insert_db()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    c = Chengdu()
    c.start()
