"""
毕节和贵阳是相同的网站
"""

from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
from urllib import parse
import re

url = 'http://www.gyfc.net.cn/2_proInfo/index.aspx'
co_index = '13'
city = '贵阳'


class Guiyang(Crawler):
    def __init__(self):
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
        }

    def start_crawler(self):
        all_url = AllListUrl(first_page_url=url, page_count_rule='总页数.*?<b>(.*?)</b>',
                             analyzer_type='regex',
                             request_method='get',
                             headers=self.headers,
                             encode='gbk')
        # 所有分页
        page_count = all_url.get_page_count()
        all_url_list = []
        for i in range(1, page_count + 1):
            all_url_list.append('http://www.gyfc.net.cn/2_proInfo/index.aspx/?page=' + str(i))
        print(all_url_list)

        build_list_url = self.get_comm_info(all_url_list)
        # 获取所有楼栋列表页 http://www.gyfc.net.cn/pro_query/index.aspx?yszh=2017005&qu=2
        all_bu_detail_url = self.get_build_detail_url(build_list_url)
        house_url_list = self.get_build_detail(all_bu_detail_url)
        ture_house_url_list = self.get_true_house_url(house_url_list)

        self.get_house_detail(ture_house_url_list)
        print('小区数据入库成功')

    def get_house_detail(self, house_url_list):
        for i in house_url_list:
            h = House(co_index)
            h.bu_id = 'yszh=(.*?)".*?id'
            h.ho_num = 'span class=\'.*?>(.*?)<'
            h.info = 'title=\'(.*?)\'>.*?<span'

            data_list = h.to_dict()
            p = ProducerListUrl(headers=self.headers,
                                analyzer_rules_dict=data_list,
                                page_url=i,
                                analyzer_type='regex',
                                request_type='get',
                                encode='gbk', )
            p.get_details()

    def get_true_house_url(self, complete_url_list):
        true_list = []
        for k in complete_url_list:
            p = ProducerListUrl(current_url_rule="src='(index/floorView\.aspx.*?)'",
                                page_url=k,
                                headers=self.headers,
                                analyzer_type='regex',
                                request_type='get',
                                encode='gbk',
                                )
            true_url_list = p.get_current_page_url()
            new_url_list = []
            for i in true_url_list:
                qu = re.findall('qu=(.*?)&', i)[0]
                url_encode = parse.quote(qu)
                replace_str = re.sub(qu, url_encode, i)
                new_url_list.append('http://www.gyfc.net.cn/pro_query/' + replace_str)
            true_list = new_url_list + true_list
        return true_list

    def get_build_detail(self, all_house_detail_url):
        house_url = []
        for i in all_house_detail_url:
            b = Building(co_index)
            b.co_name = '项目名称：<span.*?">(.*?)</span>'
            b.bu_id = '>预\(销\)售证号.*?"20">(.*?)&nbsp'  # 楼栋id，预(销)售证号
            b.bu_build_size = '1_info_all1_listJZMJ">(.*?)</span>'  # 建筑面积
            b.size = '1_info_all1_litZDMJ">(.*?)</span>'  # 占地面积
            b.bu_pre_sale = '>预\(销\)售证号.*?"20">(.*?)&nbsp'  # 预(销)售证号
            b.bo_develops = '>开发商.*?height="20">(.*?)</td>'  # 开发商
            b.bo_build_start_time = '开工时间(.*?),'  # 开工时间
            b.bo_build_end_time = '竣工时间(.*?)</sp'  # 竣工时间

            current_url_rule = '(FloorList\.aspx?.*?)">'  # 楼层表

            data_list = b.to_dict()
            p = ProducerListUrl(headers=self.headers,
                                analyzer_rules_dict=data_list,
                                page_url=i,
                                analyzer_type='regex',
                                request_type='get',
                                encode='gbk',
                                current_url_rule=current_url_rule)
            url_list = p.get_details()
            complete_url_list = []
            for k in url_list:
                complete_url_list.append('http://www.gyfc.net.cn/pro_query/' + k)
            house_url = house_url + complete_url_list

        return house_url

    def get_build_detail_url(self, build_list_url):
        bu_url = []
        for i in build_list_url:
            p = ProducerListUrl(
                current_url_rule='//*[@id="proInfodetail_panResult"]/table/tr/td/div/table/tr/td[1]/table/tr[1]/td[3]/a/@href',
                analyzer_type='xpath',
                headers=self.headers,
                encode='gbk',
                page_url=i)
            all_build_detail_url = p.get_current_page_url()
            bu_url = bu_url + all_build_detail_url
        return bu_url

    def get_comm_info(self, all_url_list):
        url_list = []
        for i in all_url_list:
            c = Comm(co_index)
            c.co_name = '>楼盘名称.*?auto">(.*?)&nbsp'  # 15个匹配结果
            c.co_id = 'margin: 8px"><a href="http://www\.gyfc\.net\.cn/2_proInfo/LoupanDetail\.aspx\?lpid=(.*?)".*?查看详细'
            c.co_address = '>楼盘地址.*?<td>(.*?)&nbsp'

            data_list = c.to_dict()

            p = ProducerListUrl(page_url=i,
                                request_type='get', encode='gbk',
                                current_url_rule='margin: 8px"><a href="(.*?)".*?查看详细',
                                analyzer_rules_dict=data_list,
                                analyzer_type='regex',
                                headers=self.headers)
            current_url_list = p.get_details()
            url_list = current_url_list + url_list
        return url_list
