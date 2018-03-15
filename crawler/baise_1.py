"""
url = http://www.bsfcj.com/PubInfo/HouseSource.asp?page=1&xm_xzqy=&xm_xmmc=&xm_xmdz=&xm_kfs=&xm_fwhx=
city: 百色
CO_INDEX: 1
author: 周彤云
小区数：99
time:2018-02-11
"""

import requests
from lxml import etree
from comm_info import Comm, Building, House
from crawler_base import Crawler
import re
from retry import retry


class Baise(Crawler):
    url = 'http://www.bsfcj.com/PubInfo/HouseSource.asp'  # 类属性

    def start_crawler(self):
        self.baise_start()

    @retry(tries=3)
    def get_all_page(self):
        try:
            res = requests.get(url=self.url)
            html = res.content.decode('gb2312', 'ignore').replace('\n', '').replace('\t', '').replace('\r', '').replace(
                ' ', '')
            page = re.search(r'/(\d+)</strong>页', html).group(1)
            return page
        except Exception as e:
            print('retry')
            raise

    @retry(tries=3)
    def baise_start(self):
        try:
            page = self.get_all_page()
            for i in range(1, int(page) + 1):
                res = requests.get(self.url + '?page=' + str(i))
                html = res.content.decode('gb2312', 'ignore')
                com_list = re.findall(r'height="25"><a href="(.+)">', html)

                for i in com_list:
                    comm = Comm(1)
                    href = 'http://www.bsfcj.com/PubInfo/' + i
                    # href = 'http://www.bsfcj.com/PubInfo/' + 'lpxx.asp?qyxmbm=DBDHDADCDADADADFDDDBDCDJ000001'
                    if not href:
                        continue
                    comm = self.get_comm_detail(href, comm)
                    comm.insert_db()
        except Exception as e:
            print('retry')

    @retry(tries=3)
    def get_comm_detail(self, href, comm):
        try:
            res = requests.get(url=href)
            co_id = res.url
            co_id = co_id.split('=')[1]  # 小区id
            html = res.content.decode('gb2312', 'ignore').replace('\n', '').replace('\t', '').replace('\r', '').replace(
                ' ', '')
            # 获取小区详情字段
            co_name = re.search(
                r'class="padingleft3px">(.*)?</td><tdwidth="1"rowspan="13"align="right"bgcolor="#CECFCE"><palign="left"></td><tdwidth="2"rowspan="13"align="right"bgcolor="#FFFFFF">',
                html).group(1)  # 小区名
            co_adress = re.search(
                r'<tdalign="left"class="padingleft3px">(.*)?</td></tr><tr><tdheight="25"align="right"><palign="left">项目开发形式：',
                html).group(1)  # 地址
            co_investor = re.search(
                r'投资商：</td><tdalign="left"class="padingleft3px">(.*)?</td></tr><tr><tdheight="25"align="right"><palign="left">是否在建：',
                html).group(1)  # 投资商
            co_is_build = re.search(
                r'是否在建：</td><tdalign="left"class="padingleft3px">(.*)?</td><tdalign="right"><palign="left">项目类型：',
                html).group(1)  # 是否在建
            if '在建' in co_is_build:
                co_is_build = '0'
            elif '竣工' in co_is_build:
                co_is_build = '1'
            else:
                co_is_build = None
            co_type = re.search(
                r'项目类型：</td><tdalign="left"class="padingleft3px">(.*)?</td></tr><tr><tdheight="25"align="right"><palign="left">项目代理：',
                html).group(1)  # 项目类型
            co_size = re.search(
                r'占地面积：</td><tdalign="left"class="padingleft3px">(.*)?m<sup>2</sup></td></tr><tr><tdheight="25"align="right"><palign="left">竣工日期（计划）',
                html).group(1)  # 占地面积
            # print(co_size)
            co_build_size = re.search(
                r'建筑面积：</td><tdalign="left"class="padingleft3px">(.*)?m<sup>2</sup></td></tr><tr><tdheight="25"align="right"><palign="left">容积率',
                html).group(1)  # 建筑面积
            co_build_start_time = re.search(
                r'开工日期（计划）：</td><tdalign="left"class="padingleft3px">(.*)?</td><tdalign="right"><palign="left">占地面积',
                html).group(1)  # 开工时间
            co_build_end_time = re.search(
                r'竣工日期（计划）：</td><tdalign="left"class="padingleft3px">(.*)?</td><tdheight="25"align="right"><palign="left">建筑面积',
                html).group(1)  # 竣工时间
            co_volumetric = re.search(
                r'容积率：</td><tdalign="left"class="padingleft3px">(.*)?</td><tdalign="right"><palign="left">绿化率',
                html).group(
                1)  # 容积率
            co_green = re.search(
                r'绿化率：</td><tdalign="left"class="padingleft3px">(.*)?</td></tr><tr><tdheight="25"align="right"><palign="left">投资计划批准文件文号',
                html).group(1)  # 绿化率
            co_pre_sale = re.search(
                r'售许可证：</td><tdalign="left"class="padingleft3px"style="line-height:25px;">(.*)?</td><tdheight="25"align="right"valign="top"style="padding-top:6px;"><palign="left">',
                html).group(1).rstrip('<br/>').split('<br/>')  # 预售证书
            if not co_pre_sale:
                return comm
            co_land_use = re.search(
                r'土地使用权证：</td><tdalign="left"class="padingleft3px">(.*)?</td><tdalign="right"><palign="left">建设工程规划许可证',
                html).group(1).rstrip('<br/>').split('<br/>')  # 土地使用证
            if not co_land_use:
                return comm
            co_pre_sale_date = re.search(
                r'售许可证发证日期：</td><tdalign="left"class="padingleft3px"style="line-height:25px;">(.*?)</td></tr><tr><tdheight="25"align="right"><palign="left">土地使用权证',
                html).group(1).rstrip('<br/>').split('<br/>')  # 预售证书日期
            if not co_pre_sale_date:
                return comm
            comm.co_id = co_id
            comm.co_name = co_name
            comm.co_adress = co_adress
            comm.co_investor = co_investor
            comm.co_is_build = co_is_build
            comm.co_type = co_type
            comm.co_size = co_size
            comm.co_build_size = co_build_size
            comm.co_build_start_time = co_build_start_time
            comm.co_build_end_time = co_build_end_time
            comm.co_volumetric = co_volumetric
            comm.co_green = co_green
            comm.co_pre_sale = co_pre_sale
            comm.co_land_use = co_land_use
            comm.co_pre_sale_date = co_pre_sale_date
            # 获取楼栋超链接
            res = requests.get(url=href)
            html = res.content.decode('gb2312', 'ignore')
            tree = etree.HTML(html)
            build_url_list = tree.xpath('//tr[@bgcolor="#FFFFFF"]/td[7]')
            if not build_url_list:
                return comm
            else:
                for i in build_url_list:
                    build_url = i.xpath('p/a/@href')[0]
                    building_url = 'http://www.bsfcj.com/PubInfo/' + build_url
                    building = Building(1)
                    building_obj = self.get_build_detail(building_url, building, co_id, )
                    building_obj.insert_db()
                return comm
        except Exception as e:
            print('retry')

    @retry(tries=3)
    def get_build_detail(self, building_url, building, co_id):
        try:
            res = requests.get(url=building_url)
            html = res.content.decode('gb2312', 'ignore').replace('\n', '').replace('\r', '').replace('\t', '').replace(
                ' ', '')
            bu_id = building_url.split('=')[1].split('&')[0]  # 楼栋id
            bu_name = re.search(
                r'项目名称：</td><tdwidth="1"rowspan="6"background="images/trbg3.gif"></td><tdwidth="200"align="left"class="padingleft3px">(.*)?</td><tdwidth="1"rowspan="6"align="right"bgcolor="#CECFCE"></td><tdwidth="2"rowspan="6"align="right"bgcolor="#FFFFFF">',
                html).group(1)  # 楼栋名称
            bu_num = re.search(
                r'号：</td><tdwidth="1"rowspan="6"background="images/trbg3.gif"></td><tdalign="left"class="padingleft3px">(.*)?</td></tr><tr><tdheight="25"align="right">总&nbsp;套&nbsp;数',
                html).group(1)  # 栋号
            # print(bu_num)
            bu_all_house = re.search(
                r'总&nbsp;套&nbsp;数：</td><tdalign="left"class="padingleft3px">(.*?)</td><tdalign="right">可售套数',
                html).group(1)  # 总套数
            bu_floor = re.search(r'总层数：</td><tdalign="left"class="padingleft3px">(.*)?</td><tdalign="right">项目类型',
                                 html).group(1)  # 总层数
            bu_build_size = re.search(
                r'建筑面积：</td><tdalign="left"class="padingleft3px"><FONTcolor=#ff0000>(.*)?M&sup2;</FONT></td><tdalign="right">住宅面积'
                , html).group(1)  # 建筑面积
            bu_live_size = re.search(
                r'住宅面积：</td><tdalign="left"class="padingleft3px">(.*)?M&sup2;</td></tr><tr><tdheight="25"align="right">幢套内建筑面积',
                html).group(1)  # 住宅面积
            bu_not_live_size = re.search(
                r'非住宅面积：</td><tdalign="left"class="padingleft3px">(.*)?M&sup2;</td></tr><tr><tdheight="25"align="right">预'
                , html).group(1)  # 非住宅面积
            bu_pre_sale = re.search(r'售许可证：</td><tdalign="left"class="padingleft3px">(.*?)</td>', html).group(
                1)  # 楼栋预售证书
            bu_pre_sale_date = re.search(r'售许可证发证日期：</td><tdalign="left"class="padingleft3px">(.*?)</td>', html).group(
                1)  # 楼栋预售证书日期
            bu_price = re.search(
                r'拟销住宅价格：</td><tdbackground="images/trbg3.gif"></td><tdalign="left"class="padingleft3px">(.*)?</td><tdalign="right"bgcolor="#CECFCE"></td><tdalign="right"bgcolor="#FFFFFF"></td><tdalign="right"bgcolor="#CECFCE"></td><tdalign="right">拟销商业门面价格'
                , html).group(1).split('元')[0]  # 住宅价格
            building.co_id = co_id
            building.bu_id = bu_id
            building.bu_name = bu_name
            building.bu_num = bu_num
            building.bu_all_house = bu_all_house
            building.bu_floor = bu_floor
            building.bu_build_size = bu_build_size
            building.bu_live_size = bu_live_size
            building.bu_not_live_size = bu_not_live_size
            building.bu_price = bu_price
            # 获取房号超链接
            house_url_list = re.findall(r"window.open\('(.+?)'\)", html)
            for i in house_url_list:
                house_url = 'http://www.bsfcj.com/PubInfo/' + i
                house = House(1)
                house_obj = self.get_house_detail(house_url, house, co_id, bu_id)
                house_obj.insert_db()
            return building
        except Exception as e:
            print('retry')

    @retry(tries=3)
    def get_house_detail(self, house_url, house, co_id, bu_id):
        try:
            res = requests.get(url=house_url)
            html = res.content.decode('gb2312', 'ignore')
            tree = etree.HTML(html)
            ho_num = tree.xpath('//td[@width="82"]/text()')[0]  # 房号
            ho_floor = tree.xpath('//td[@width="72"]/text()')[0]  # 楼层
            ho_type = tree.xpath('//tr[3]/td[@bgcolor="#FFFFEE"][2]/text()')[0]  # 房屋类型
            ho_room_type = tree.xpath('//tr[3]/td[@bgcolor="#FFFFEE"][4]/text()')[0]  # 户型
            ho_build_size = tree.xpath('//tr[4]/td[2]/text()')[0].replace('M²', '')  # 建筑面积
            ho_true_size = tree.xpath('//tr[4]/td[4]/text()')[0].replace('M²', '')  # 预测套内面积
            ho_share_size = tree.xpath('//tr[5]/td[2]/text()')[0].replace('M²', '')  # 预测分摊面积
            orientation = tree.xpath('//tr[6]/td[2]/text()')[0]  # 朝向
            ho_price = tree.xpath('//tr[6]/td[4]/text()')  # 价格
            if ho_price:
                ho_price = ho_price[0].replace('元/M²', '')
            else:
                return house
            house.co_id = co_id
            house.bu_id = bu_id
            house.ho_num = ho_num
            house.ho_floor = ho_floor
            house.ho_type = ho_type
            house.ho_room_type = ho_room_type
            house.ho_build_size = ho_build_size
            house.ho_true_size = ho_true_size
            house.ho_share_size = ho_share_size
            house.orientation = orientation
            house.ho_price = ho_price
            return house
        except Exception as e:
            print('retry')


if __name__ == '__main__':
    b = Baise()
    b.baise_start()
