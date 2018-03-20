from crawler_base import Crawler
import requests
from comm_info import Comm, Building, House
import re


class Taian(Crawler):
    def __init__(self):
        self.url_now = 'https://cucc.tazzfdc.com/reisPub/pub/saleBuildingStatist'  # 现售
        self.url_now_source = 'https://cucc.tazzfdc.com/reisPub/pub/saleBuildingStatist'

        self.url_future = 'https://cucc.tazzfdc.com/reisPub/pub/preSaleBuildingStatist'  # 预售
        self.url_future_source = 'https://cucc.tazzfdc.com/reisPub/pub/preSaleBuildingStatist'

        self.co_index = 50
        self.headers = {
            'Cookie': 'JSESSIONID=027564E74D737A71A8DA9C12F9CE9DAD-n2; pubDistrict=370900'
        }

    def start_crawler(self):
        now_page_count = self.get_count(self.url_now)
        future_page_count = self.get_count(self.url_future)

        print(now_page_count)
        all_now_list_url = self.get_all_comm_info(self.url_now_source, now_page_count,
                                                  'https://cucc.tazzfdc.com/reisPub/pub/saleProjectInfo?')
        all_future_list_url = self.get_all_comm_info(self.url_future_source, future_page_count,
                                                     'https://cucc.tazzfdc.com/reisPub/pub/projectInfo?')

        house_url_list = self.get_build_url(all_now_list_url + all_future_list_url)

    def get_build_url(self, all_list_url):
        # all_list_url 为dict [{'area':'', 'url':''},{}]
        # 存储小区的信息，存储楼栋的信息
        for i in all_list_url:
            res = requests.get(url=i['url'], )
            html_str = res.content.decode()
            c = Comm(self.co_index)
            c.area = i['area']
            c.co_name = re.search('项目名称：.*?left">(.*?)</td>', html_str, re.S | re.M).group(1)
            c.co_owner = re.search('所有权证号：.*?left">(.*?)</td>', html_str, re.S | re.M).group(1)
            c.co_land_use = re.search('土地使用权证：.*?left">(.*?)</td>', html_str, re.S | re.M).group(1)
            c.co_land_type = re.search('土地权证类型：.*?left">(.*?)</td>', html_str, re.S | re.M).group(1)
            c.insert_db()


            # todo 找到楼栋重新写
            for k in re.findall("buildingInfo\('(.*?)',(.*?)\).>(.*?)</a>", html_str, re.S | re.M):
                b = Building(self.co_index)
                b.co_name = re.search('项目名称：.*?left">(.*?)</td>', html_str, re.S | re.M).group(1)
                b.bu_num = k[0][3]
                b.bu_build_size = ''


    def get_all_comm_info(self, url, now_page_count, mosaic):
        url_list = []
        for i in range(1, int(now_page_count) + 1):
            data = {
                'pageNo': i
            }
            res = requests.post(url=url, data=data, headers=self.headers)
            print(res.content.decode())
            html_str = res.content.decode()
            page_url_list = []
            for k in re.findall('<tr onmouseover.*?</tr>', html_str, re.S | re.M):
                area = re.search('<div.*?>(.*?)</div>', k, re.S | re.M).group(1)
                href = re.findall("projectInfo\('(.*?)','(.*?)'\)", k, re.S | re.M)
                url = mosaic + 'id=' + href[0][0] + '&cid=' + href[0][1]
                area_url_dict = {
                    'area': area,
                    'url': url
                }
                page_url_list.append(area_url_dict)

            url_list = page_url_list + url_list
            break
        return url_list

    def get_count(self, url):
        res = requests.get(url, headers=self.headers)
        splited_str = re.search('上一页.*?下一页', res.content.decode(), re.S | re.M).group()
        num_list = re.findall('\d+', splited_str, re.S | re.M)
        return max(num_list)
