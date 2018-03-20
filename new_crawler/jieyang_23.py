"""
url = http://www.jyfg.cn/HouseWebSetup/PublicReport/PublicInfoIndex.aspx
city : 揭阳
CO_INDEX : 23
小区数量：109
"""
from comm_info import Comm, Building, House
import re, requests
from lxml import etree

url = 'http://www.jyfg.cn/HouseWebSetup/PublicReport/PublicInfoIndex.aspx'
co_index = '23'
city = '揭阳'


class Jieyang(object):
    def __init__(self):
        pass

    def start_crawler(self):
        response = requests.get(url)
        html = response.text
        tree = etree.HTML(html)
        comm_list = tree.xpath('//tr[@class="Row"]/td[1]/text()')
        co_develops_list = tree.xpath('//tr[@class="Row"]/td[3]/text()')
        co_address_list = tree.xpath('//tr[@class="Row"]/td[8]/text()')
        co_open_time_list = tree.xpath('//tr[@class="Row"]/td[9]/text()')
        co_pre_sale_list = tree.xpath('//tr[@class="Row"]/td[5]/text()')
        co_all_house_list = tree.xpath('//tr[@class="Row"]/td[11]/text()')
        co_build_size_list = tree.xpath('//tr[@class="Row"]/td[10]/text()')
        co_name_list = tree.xpath('//tr[@class="Row"]/td[4]/text()')
        for co in range(0, len(comm_list)):
            comm = Comm(co_index)
            comm_url = 'http://www.jyfg.cn/HouseWebSetup/PublicReport/PreSellLicenceDetailInfo.aspx?PreSellLicenceSN=' + \
                       comm_list[
                           co]
            result = requests.get(comm_url)
            html_build = result.text
            tree = etree.HTML(html_build)
            build_list = tree.xpath('//tr[@class="Row"]/td[2]/text()')
            bu_name_list = tree.xpath('//tr[@class="Row"]/td[4]/text()')
            bu_floor_list = tree.xpath('//tr[@class="Row"]/td[5]/text()')
            area = tree.xpath('//*[@id="LabSCFW"]/text()')[0]
            comm.co_id = comm_list[co]
            comm.area = area
            comm.co_develops = co_develops_list[co]
            comm.co_address_list = co_address_list[co]
            comm.co_open_time_list = co_open_time_list[co]
            comm.co_pre_sale_list = co_pre_sale_list[co]
            comm.co_all_house_list = co_all_house_list[co]
            comm.co_build_size_list = co_build_size_list[co]
            comm.co_develops = co_develops_list[co]
            comm.co_name = co_name_list[co]
            comm.insert_db()
            for bu in range(0, len(build_list)):
                building = Building(co_index)
                build_url = 'http://www.jyfg.cn/HouseWebSetup/PublicReport/PubRptHouseList.aspx?BuildingSN=' + \
                            build_list[bu]
                building.bu_name = bu_name_list[bu]
                building.bu_floor = bu_floor_list[bu]
                building.co_id = comm.co_id
                building.bu_id = build_list[bu]
                building.insert_db()
                resp = requests.get(build_url)
                html = resp.text
                house_list = re.findall('房号:<a href="(.*?)"', html)
                for ho in house_list:
                    house = House(co_index)
                    house_url = 'http://www.jyfg.cn/HouseWebSetup/PublicReport/' + ho
                    respon = requests.get(house_url)
                    html = respon.text
                    house.bu_id = building.bu_id
                    house.ho_name = re.search('房号:.*?<span.*?>(.*?)<', html, re.M | re.S).group(1)
                    house.ho_build_size = re.search('预测建筑面积:.*?<span.*?>(.*?)<', html, re.M | re.S).group(1)
                    house.ho_true_size = re.search('预测套内面积:.*?<span.*?>(.*?)<', html, re.M | re.S).group(1)
                    house.ho_share_size = re.search('预测分摊面积:.*?<span.*?>(.*?)<', html, re.M | re.S).group(1)
                    house.ho_type = re.search('房屋用途:.*?<span.*?>(.*?)<', html, re.M | re.S).group(1)
                    house.ho_room_type = re.search('户型结构:.*?<span.*?>(.*?)<', html, re.M | re.S).group(1)
                    house.insert_db()


if __name__ == '__main__':
    j = Jieyang()
    j.start_crawler()
