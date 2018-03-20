"""
url = http://www.gzbjfc.com/House.aspx
city : 毕节
CO_INDEX : 3
小区数量：
"""
from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import requests, re

url = 'http://www.gzbjfc.com/House.aspx'
co_index = '3'
city = '毕节'


class Bijie(Crawler):
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
                       page_count_rule='下页</a>.*?page=(.*?)"',
                       )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            all_page_url = url + '?page=' + str(i)
            response = requests.get(all_page_url, headers=self.headers)
            html = response.text
            comm_url_list = re.findall('项目名称：.*?href="(.*?)"', html, re.S | re.M)
            self.get_comm_info(comm_url_list)

    def get_comm_info(self, comm_url_list):
        for i in comm_url_list:
            try:
                comm = Comm(co_index)
                comm_url = 'http://www.gzbjfc.com/' + i
                comm.co_name = 'cph_hif1_xmmc.*?<.*?>(.*?)<'
                comm.co_pre_sale = 'cph_hif1_xsxkz.*?<.*?>(.*?)<'
                comm.co_address = 'cph_hif1_zl.*?<.*?>(.*?)<'
                comm.co_develops = 'cph_hif1_kfs.*?<.*?>(.*?)<'
                comm.co_handed_time = 'cph_hif1_jfsj.*?<.*?>(.*?)<'
                comm.co_build_size = 'cph_hif1_jzmj.*?>(.*?)<'
                comm.co_all_house = 'cph_hif1_fwts.*?>(.*?)<'
                comm.co_id = 'hdl1_hfYszh" value="(.*?)"'
                p = ProducerListUrl(page_url=comm_url,
                                    request_type='get', encode='utf-8',
                                    analyzer_rules_dict=comm.to_dict(),
                                    analyzer_type='regex',
                                    headers=self.headers)
                p.get_details()
                # 楼栋信息
                build_url = comm_url.replace('Info', 'Building')
                self.get_build_info(build_url)
            except Exception as e:
                print(e)

    def get_build_info(self, build_url):
        build = Building(co_index)
        build.bu_id = 'cph_hb1_dg1.*?center.*?center.*?<td>(.*?)<'
        build.co_id = 'hdl1_hfYszh" value="(.*?)"'
        build.bu_num = 'cph_hb1_dg1.*?center.*?center.*?<td>.*?<td>(.*?)<'
        build.bu_all_house = 'cph_hb1_dg1.*?center.*?center.*?<td>.*?<td>.*?<td>(.*?)<'
        p = ProducerListUrl(page_url=build_url,
                            request_type='get', encode='utf-8',
                            analyzer_rules_dict=build.to_dict(),
                            current_url_rule='cph_hb1_dg1.*?<a.*?href="(.*?)"',
                            analyzer_type='regex',
                            headers=self.headers)
        house_url_list = p.get_details()
        self.get_house_info(house_url_list)

    def get_house_info(self, house_url_list):
        for i in house_url_list:
            try:
                dong_ID = re.search('dongID=(.*?)$', i).group(1)
                yszh = re.search('yszh=(.*?)&', i).group(1)
                house_url = 'http://www.gzbjfc.com/Controls/HouseControls/FloorView.aspx?dongID=' + dong_ID + '&qu=%E6%AF%95%E8%8A%82&yszh=' + yszh + '&zhlx=xs&danyuan=all'
                house = House(co_index)
                house.bu_id = 'dongID=(.*?)&'
                house.ho_name = '<span.*?>(.*?)<'
                house.info = "<div class=.*?title='(.*?)'.*?<span"
                p = ProducerListUrl(page_url=house_url,
                                    request_type='get', encode='utf-8',
                                    analyzer_rules_dict=house.to_dict(),
                                    analyzer_type='regex',
                                    headers=self.headers)
                p.get_details()
            except Exception as e:
                print(e)
