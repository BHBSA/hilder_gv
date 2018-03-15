"""
url = http://www.jjzzfdc.com.cn/WebClient/ClientService/frmYsxk_more.aspx?qcount=10000&pcount=33
city : 九江
CO_INDEX : 25
小区数量：345
"""
from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import requests, re

url = 'http://www.jjzzfdc.com.cn/WebClient/ClientService/frmYsxk_more.aspx?qcount=10000&pcount=33'
co_index = '25'
city = '九江'


class Jiujiang(object):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
            'Referer': 'http://www.jjzzfdc.com.cn/WebClient/ClientService/frmYsxk_more.aspx?qcount=10000&pcount=33'

        }

    def start_crawler(self):
        b = AllListUrl(first_page_url=url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='gbk',
                       page_count_rule='共(.*?)页',
                       )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            all_page_url = url + '&Page=' + str(i)
            p = ProducerListUrl(page_url=all_page_url,
                                request_type='get', encode='gbk',
                                analyzer_rules_dict=None,
                                current_url_rule="eval\('openBldg\((.*?)\)",
                                analyzer_type='regex',
                                headers=self.headers)
            comm_url_list = p.get_current_page_url()
            self.get_build_info(comm_url_list)

    def get_build_info(self, comm_url_list):
        for i in comm_url_list:
            sid = re.findall('\+(\d+)\+', i)[0]
            pid = re.findall('\+(\d+)\+', i)[1]
            build_url = 'http://www.jjzzfdc.com.cn/WebClient/ClientService/bldg_query.aspx?pid=' + pid + '&sid=' + sid
            response = requests.get(build_url)
            html = response.text
            build = Building(co_index)
            build.bu_num = re.search('楼栋座落.*?<td.*?>(.*?)<',html, re.S | re.M).group(1)
            build.insert_db()
            house_url = 'http://www.jjzzfdc.com.cn/WebClient/ClientService/proxp.aspx?key=WWW_LPB_001&params=' + sid
            result = requests.get(house_url)
            html_ = result.text
            house = House(co_index)
            ho_name_list = re.findall('<CNAME>(.*?)</CNAME>', html_, re.S | re.M)
            for index in range(len(ho_name_list)):
                house.ho_name = ho_name_list[index]

                house.insert_db()
