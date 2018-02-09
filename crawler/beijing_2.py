"""
url: http://www.bjjs.gov.cn/eportal/ui?pageId=307678
city: 北京
CO_INDEX: 2
author: 吕三利
"""
from crawler_base import Crawler
import requests
import re
import math
from comm_info import Comm, Building, House
from retry import retry
CO_INDEX = 2
class Beijing(Crawler):
    def __init__(self):
        self.url = 'http://www.bjjs.gov.cn/eportal/ui?pageId=307678'

    def start_crawler(self):
        self.start()

    @retry(tries=3)
    def get_all_page(self):
        try:
            response = requests.post(url=self.url)
            if response.status_code is 200:
                html = response.text
                page_num = re.search('总记录数:(\d+),', html).group(1)
                page = math.ceil(int(page_num) / 15)
                return page
            else:
                print('错误')
        except Exception as e:
            print('retry')
            raise

    @retry(tries=3)
    def start(self):
        try:
            page = self.get_all_page()
            for page in range(1, int(page) + 1):
                params = {'currentPage': page}
                response = requests.post(url=self.url, params=params)
                html = response.text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                self.get_comm_info(html)
        except Exception as e:
            print('retry')
            raise
    def get_comm_info(self, html):
        html_info = re.search('预售商品房住宅项目公示(.*?)</table>', html).group(1)
        comm_list = re.findall(
            '<td(.*?)ahref="(.*?)">(.*?)</a(.*?)<ahref="(.*?)">(.*?)</a></td><td(.*?)>(.*?)</td></tr>', html_info)
        for i in comm_list:
            comm = Comm()
            url = 'http://www.bjjs.gov.cn/' + i[1]
            self.get_comm_detail(url, comm)
    @retry(tries=3)
    def get_comm_detail(self, url, comm):
        try:
            response = requests.get(url=url)
            comm_html = response.text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
            co_id = re.search('projectID=(\d+)&', url).group(1)  # 小区id
            co_name = re.search('id="项目名称(.*?)>(.*?)<', comm_html).group(2)  # 小区名称
            co_address = re.search('id="坐落位置(.*?)>(.*?)<', comm_html).group(2)  # 小区地址
            co_pre_sale = re.search('id="预售许可证编号(.*?)>(.*?)<', comm_html).group(2)  # 预售证书
            co_build_size = re.search('id="准许销售面积(.*?)>(.*?)<', comm_html).group(2)  # 建筑面积
            co_develops = re.search('id="开发企业(.*?)>(.*?)<', comm_html).group(2)  # 建筑面积
            co_pre_sale_date = re.search('id="发证日期(.*?)>(.*?)<', comm_html).group(2)  # 发证日期
            comm.co_index = CO_INDEX
            comm.co_id = co_id
            comm.co_name = co_name
            comm.co_address = co_address
            comm.co_pre_sale = co_pre_sale
            comm.co_build_size = co_build_size
            comm.co_develops = co_develops
            comm.co_pre_sale_date = co_pre_sale_date
            build_info_list = re.findall(
                '--><tr><td(.*?)>(.*?)</td><(.*?)>(.*?)</td><(.*?)>(.*?)</td><(.*?)>(.*?)</td><td(.*?)>(.*?)<',
                comm_html)
            if not build_info_list:
                print('没有房屋信息')
            else:
                for i in build_info_list:
                    building = Building()
                    bu_name = i[1]  # 楼栋名称
                    bu_num = bu_name.split('#')[0]  # 楼号
                    bu_all_house = i[3]  # 总套数
                    bu_build_size = i[5]  # 面积
                    bu_price = i[9]  # 价格
                    # 给对象增加属性
                    building.bu_name = bu_name
                    building.bu_num = bu_num
                    building.bu_all_house = bu_all_house
                    building.bu_build_size = bu_build_size
                    building.bu_price = bu_price
                    building.co_id = co_id  # 小区id
                    building.co_index = CO_INDEX  # 网站id

                    build_html = re.search(r'楼盘表(.*?)个楼栋信息', comm_html).group(1)
                    build_url = re.search(r'<ahref="(.*?)">查看信息<', build_html).group(1)
                    build_id = re.search('buildingId=(.*?)$',build_url).group(1)
                    bu_floor = self.get_build_info(build_url, co_id)
                    building.bu_id = build_id  #楼栋id
                    building.bu_floor = bu_floor  # 楼层

                    building.insert_db()
            comm.insert_db()
        except Exception as e:
            print('retry')
            raise

    @retry(tries=3)
    def get_build_info(self, build_url,co_id):
        try:
            url = 'http://www.bjjs.gov.cn' + build_url
            response = requests.get(url)
            html = response.text.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
            house_url_list = re.findall(r'■(.*?)<ahref="(.*?)">(.*?)</a>',html)
            bu_id = re.search(r'buildingId=(.*?)$',build_url).group(1)
            bu_floor = re.search(r'地上:(\d+)层',html).group(1)
            for i in house_url_list:
                house = House()
                house_url = i[1]
                house_data = self.get_house_info(house_url,house)
                house_data.co_id = co_id
                house_data.bu_id = bu_id
                house_data.insert_db()
            return bu_floor
        except Exception as e:
            print('retry')
            raise
    @retry(tries=3)
    def get_house_info(self,house_url,house):
        try:
            url = 'http://www.bjjs.gov.cn' + house_url
            response = requests.get(url)
            html = response.text.replace('\n','').replace('\r','').replace('\t','').replace(' ','')
            ho_name = re.search('"font-size:18px;font-family:黑体;font-family:verdana;color:red;">(.*?)<',html).group(1) # 房号：3单元403
            ho_type = re.search('规划设计用途</td><(.*?)>(.*?)<',html).group(2) # 房屋类型：普通住宅 / 车库仓库
            ho_room_type = re.search('户　　型</td><(.*?)>(.*?)<',html).group(2) # 户型：一室一厅
            ho_build_size = re.search('>建筑面积</td><(.*?)>(.*?)平方米<',html).group(2) # 建筑面积
            ho_true_size = re.search('>套内面积</td><(.*?)>(.*?)平方米<',html).group(2)  # 预测套内面积,实际面积
            ho_price = re.search('>按建筑面积拟售单价</td><(.*?)>(.*?)元/平方米<',html).group(2)  # 价格
            ho_share_size = float(ho_build_size) - float(ho_true_size)  # 分摊面积
            ho_floor = re.search('\d',ho_name).group()  # 楼层
            ho_num = re.search('houseId=(.*?)&',house_url).group(1)  # 房号id
            house.co_index = CO_INDEX
            house.ho_name = ho_name
            house.ho_type = ho_type
            house.ho_room_type = ho_room_type
            house.ho_build_size = ho_build_size
            house.ho_true_size = ho_true_size
            house.ho_price = ho_price
            house.ho_share_size = ho_share_size
            house.ho_floor = ho_floor
            house.ho_num = ho_num
            return house
        except Exception as e:
            print('retry')
            raise

if __name__ == '__main__':
    b = Beijing()
    b.start_crawler()
