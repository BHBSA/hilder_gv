"""
url = http://www.kmhouse.org/moreHousePriceList.asp?page=1
city : 昆明
CO_INDEX : 26
小区数量：1180
"""
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
import requests, re
from retry import retry

url = 'http://www.kmhouse.org/moreHousePriceList.asp?page=1'
co_index = '26'
city = '昆明'

count = 0


class Kunming(object):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
        }

    @retry(tries=3)
    def start_crawler(self):
        b = AllListUrl(first_page_url=url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='gbk',
                       page_count_rule='strong>1/(.*?)<',
                       headers=self.headers
                       )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            try:
                index_url = 'http://www.kmhouse.org/moreHousePriceList.asp?page=' + str(i)
                response = requests.get(url=index_url, headers=self.headers)
                html = response.content.decode('gbk')
                comm_url_list = re.findall("cellspacing='3'.*?<a href='(.*?)'", html)
                self.get_comm_info(comm_url_list)
            except Exception as e:
                continue

    @retry(tries=3)
    def get_comm_detail(self, comm_detail_url):
        try:
            comm = Comm(co_index)
            comm_url = 'http://www.kmhouse.org' + comm_detail_url
            response = requests.get(comm_url, headers=self.headers)
            html = response.content.decode('gbk')
            co_id = re.search('Preid=(.*?)&', comm_detail_url).group(1)
            co_name = re.search('楼盘名称.*?<td.*?>(.*?)<', html, re.S | re.M).group(1)
            area = re.search('所在地区.*?<td.*?>(.*?)<', html, re.S | re.M).group(1)
            co_address = re.search('楼盘地址.*?<td.*?>(.*?)<', html, re.S | re.M).group(1)
            co_pre_sale = re.search('预售证号.*?<td.*?>(.*?)<', html, re.S | re.M).group(1)
            co_volumetric = re.search('容&nbsp;积&nbsp;率.*?<td.*?>(.*?)<', html, re.S | re.M).group(1)
            co_green = re.search('绿&nbsp;化&nbsp;率.*?<td.*?>(.*?)<', html, re.S | re.M).group(1)
            co_build_start_time = re.search('开工时间.*?<td.*?>(.*?)<', html, re.S | re.M).group(1)
            comm.co_name = co_name
            comm.area = area
            comm.co_id = co_id
            comm.co_address = co_address
            comm.co_pre_sale = co_pre_sale
            comm.co_volumetric = co_volumetric
            comm.co_green = co_green
            comm.co_build_start_time = co_build_start_time
            comm.insert_db()
            global count
            count += 1
            print(count)
        except Exception as e:
            print(e)

    @retry(tries=3)
    def get_comm_info(self, comm_url_list):
        for i in comm_url_list:
            try:
                comm_url = "http://www.kmhouse.org" + i
                co_id = re.search("PreId=(.*?)&", i).group(1)
                response = requests.get(comm_url, headers=self.headers)
                html = response.text
                build_list = re.findall("</option><option value='(.*?)'", html, re.S | re.M)
                comm_detail_url = re.findall('linkone" href="(.*?)"', html, re.S | re.M)[0]
                self.get_comm_detail(comm_detail_url)
                for index in range(len(build_list)):
                    try:
                        build = Building(co_index)
                        build_url = 'http://www.kmhouse.org/newhouse/houseprice.asp?PreId=' + co_id + '&Aid=1'
                        data = {
                            'bid': build_list[index],
                            'mess': '1',
                            'aid': '1',
                            'preid': co_id,
                            'issearch': 'yes'
                        }
                        response = requests.post(build_url, data=data, headers=self.headers)
                        html_new = response.content.decode('gbk')
                        bu_num = re.findall('</option><option value=.*?>(.*?[栋幢座])', html_new, re.S | re.M)
                        build.bu_num = bu_num[index]
                        build.bu_id = build_list[index]
                        build.co_id = co_id
                        build.insert_db()
                        all_page = re.search('页次:1/(.*?)\n', html_new).group(1)
                        for i in range(1, int(all_page)):
                            try:
                                house_url = 'http://www.kmhouse.org/newhouse/houseprice.asp?page=' + str(
                                    i) + '&aid=1&preid=' + co_id + '&bid=' + build_list[index] + '&issearch=yes'
                                response = requests.get(house_url, headers=self.headers)
                                html_house = response.content.decode('gbk')
                                ho_name_list = re.findall("color='blue'>(.*?)<", html_house)
                                co_build_structural_list = re.findall("color='blue'>.*?center >(.*?)<", html_house)
                                co_use_list = re.findall(
                                    "color='blue'>.*?center.*?center.*?center >(.*?)<", html_house)
                                ho_build_size_list = re.findall(
                                    "color='blue'>.*?center.*?center.*?center.*?center >(.*?)<",
                                    html_house)
                                ho_true_size_list = re.findall(
                                    "color='blue'>.*?center.*?center.*?center.*?center.*?center >(.*?)<",
                                    html_house)
                                for i in range(0, len(ho_name_list)):
                                    try:
                                        house = House(co_index)
                                        house.ho_name = ho_name_list[i]
                                        house.co_build_structural = co_build_structural_list[i]
                                        house.co_use = co_use_list[i]
                                        house.ho_build_size = ho_build_size_list[i]
                                        house.ho_true_size = ho_true_size_list[i]
                                        house.bu_id = build_list[index]
                                        house.insert_db()
                                    except Exception as e:
                                        print(e)
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
                        continue
            except Exception as e:
                continue
