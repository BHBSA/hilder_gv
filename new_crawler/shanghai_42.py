from crawler_base import Crawler
from producer import ProducerListUrl
from comm_info import Comm, Building, House
import requests
import re


class Shanghai(Crawler):
    def __init__(self):
        self.url = 'http://www.fangdi.com.cn/complexpro.asp'
        self.co_index = 42
        self.area_list = [1, 10, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    def start_crawler(self):
        # 小区列表页url
        comm_list_url = self.get_all_comm_list_url()
        build_url_list = self.get_build_url_list(comm_list_url)

    def get_build_url_list(self, comm_list_url):
        all_url = []
        for i in comm_list_url:
            c = Comm(self.co_index)
            c.co_name = 'href=proDetail\.asp\?projectID.*?>(.*?)<'  # 项目名称
            c.co_address = 'href=proDetail\.asp\?projectID.*?padding:3">(.*?)</td>'  # 项目地址
            c.co_size = 'href=proDetail\.asp\?projectID.*?padding:3">.*?</td>.*?</td>.*?padding:3">(.*?)</td>'  # 总面积
            c.area = 'href=proDetail\.asp\?projectID.*?padding:3">.*?</td>.*?</td>.*?padding:3">.*?</td>.*?padding:3">(.*?)</td>'  # 所在区县
            current_url_rule = 'href=(proDetail\.asp\?projectID.*?)>'  # 下一页的url
            data_dict = c.to_dict()
            p = ProducerListUrl(analyzer_rules_dict=data_dict,
                                page_url=i,
                                analyzer_type='regex',
                                request_type='get',
                                encode='gbk',
                                current_url_rule=current_url_rule)
            url_list = p.get_details()
            #  拼接url
            true_url_list = []
            for k in url_list:
                true_url_list.append('http://www.fangdi.com.cn/' + k)
            all_url = all_url + true_url_list
        # print(all_url)
        return all_url

    def get_all_comm_list_url(self):
        all_comm_list_url = []
        # 获取所有的地区
        for i in self.area_list:
            data = {'districtID': i}
            res = requests.post(url='http://www.fangdi.com.cn/complexPro.asp', data=data)
            html_str = res.content.decode('gbk')
            # 根据返回结果 获取每个地区的返回分页
            url_list = re.findall('"(/complexpro.*?)">', html_str, re.S | re.M)
            true_url_list = []
            for i in url_list:
                true_url_list.append('http://www.fangdi.com.cn' + i)
            # print(true_url_list)
            all_comm_list_url = all_comm_list_url + true_url_list
            break
        return all_comm_list_url
