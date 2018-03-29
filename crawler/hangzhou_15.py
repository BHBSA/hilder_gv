"""
url = http://www.tmsf.com/newhouse/property_searchall.htm
city：杭州
CO_INDEX: 15
小区数：2066
"""

from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import requests, re

url = 'http://www.tmsf.com/newhouse/property_searchall.htm'
co_index = '15'
city = '杭州'

count = 0


class Hangzhou(Crawler):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
        }

    def start_crawler(self):
        b = AllListUrl(first_page_url=url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='utf-8',
                       page_count_rule='green1">1/(.*?)<',
                       )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            all_url = 'http://www.tmsf.com/newhouse/property_searchall.htm?&page=' + str(i)
            try:
                response = requests.get(all_url, headers=self.headers, timeout=5)
            except Exception as e:
                print(e)
                continue
            html = response.text
            comm_url_list = re.findall('build_word01" onclick="toPropertyInfo\((.*?)\);', html, re.S | re.M)
            self.get_comm_info(comm_url_list)

    def get_comm_info(self, comm_url_list):
        for i in comm_url_list:
            try:
                code = i.split(',')
                comm_url = 'http://www.tmsf.com/newhouse/property_' + code[0] + '_' + code[1] + '_info.htm'
                comm = Comm(co_index)
                comm.co_name = 'buidname.*?>(.*?)<'
                comm.co_address = '--位置行--.*?<span.*?title="(.*?)"'
                comm.co_build_type = '建筑形式：<.*?>(.*?)<'
                comm.co_develops = '项目公司：<.*?>(.*?)<'
                comm.co_volumetric = '容 积 率：</span>(.*?)<'
                comm.co_green = '绿 化 率：</span>(.*?)<'
                comm.co_size = '占地面积：</span>(.*?)<'
                comm.co_build_size = '总建筑面积：</span>(.*?)<'
                comm.co_all_house = '总户数：</span>(.*?)<'
                comm.co_id = 'info" href="/newhouse/property_(.*?)_info'
                p = ProducerListUrl(page_url=comm_url,
                                    request_type='get', encode='utf-8',
                                    analyzer_rules_dict=comm.to_dict(),
                                    current_url_rule='一房一价<.*?href="(.*?)"',
                                    analyzer_type='regex',
                                    headers=self.headers)
                build_all_url = p.get_details()
                global count
                count += 1
                print(count)
                self.get_build_info(build_all_url)
            except Exception as e:
                print(e)

    def get_build_info(self, build_all_url):
        bu_all_url_list = {}
        for i in build_all_url:
            build_url = 'http://www.tmsf.com/' + i
            response = requests.get(build_url)
            html = response.text
            build_code_list = re.findall("javascript:doPresell\('(.*?)'\)", html)
            co_id = re.findall('id="sid" value="(.*?)"', html)
            if not co_id:
                continue
            for i in build_code_list:
                try:
                    build = Building(co_index)
                    build_num_url = 'http://www.tmsf.com/newhouse/property_330184_10442053_control.htm?presellid=' + i
                    build.co_id = 'search" name="search" action="/newhouse/property_(.*?)_control'
                    build.bu_num = 'javascript:doBuilding.*?>(.*?)<'
                    p_2 = ProducerListUrl(page_url=build_num_url,
                                          request_type='get', encode='utf-8',
                                          analyzer_rules_dict=build.to_dict(),
                                          current_url_rule="javascript:doBuilding\('(.*?)'",
                                          analyzer_type='regex',
                                          headers=self.headers)
                    build_num_list = p_2.get_details()
                    for i in build_num_list:
                        bu_all_url_list[i] = co_id[0]
                except Exception as e:
                    print(e)
                self.get_house_info(bu_all_url_list)

    def get_house_info(self, bu_all_url_list):
        for i in bu_all_url_list:
            try:
                house_url = 'http://www.tmsf.com/newhouse/NewPropertyHz_showbox.jspx?buildingid=' + i + '&sid=' + \
                            bu_all_url_list[i]
                house = House(co_index)
                house.bu_id = 'buildingid":(.*?),'
                house.co_build_size = 'builtuparea":(.*?),'
                house.ho_price = 'declarationofroughprice":(.*?),'
                house.ho_name = 'houseno":(.*?),'
                house.ho_true_size = 'setinsidefloorarea":(.*?),'
                house.ho_share_size = 'poolconstructionarea":(.*?),'
                house.ho_type = 'houseusage":(.*?),'
                p_2 = ProducerListUrl(page_url=house_url,
                                      request_type='get', encode='utf-8',
                                      analyzer_rules_dict=house.to_dict(),
                                      analyzer_type='regex',
                                      headers=self.headers)
                p_2.get_details()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    b = Hangzhou()
    b.start_crawler()
