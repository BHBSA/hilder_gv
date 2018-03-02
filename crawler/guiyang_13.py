from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import requests

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
        page_count = all_url.get_page_count()
        all_url_list = []
        for i in range(1, page_count + 1):
            all_url_list.append('http://www.gyfc.net.cn/2_proInfo/index.aspx/page=' + str(i))
        print(all_url_list)

        build_list_url = self.get_comm_info(all_url_list)
        # 获取所有楼栋列表页 http://www.gyfc.net.cn/pro_query/index.aspx?yszh=2017005&qu=2
        all_house_detail_url = self.get_build_detail_url(build_list_url)
        house_url_list = self.get_build_detail(all_house_detail_url)

        p = ProducerListUrl(co_index)
        ture_house_url_list = p.get_current_page_url(house_url_list)
        self.get_house_detail(ture_house_url_list)
        print('小区数据入库成功')

    def get_house_detail(self, house_url_list):
        h = House(co_index)
        h.bu_id = '<title>.*?[(.*?)].*?</title>'
        h.ho_num = ''

        data_list = h.to_dict()
        p = ProducerListUrl(headers=self.headers,
                            analyzer_rules_dict=data_list,
                            list_page_url=house_url_list,
                            analyzer_type='regex',
                            request_type='get',
                            encode='gbk',)
        p.get_details()


    def get_build_detail(self, all_house_detail_url):
        b = Building(co_index)
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
                            list_page_url=all_house_detail_url,
                            analyzer_type='regex',
                            request_type='get',
                            encode='gbk',
                            current_url_rule=current_url_rule)
        url_list = p.get_details()
        complete_url_list = []
        for i in url_list:
            complete_url_list.append('http://www.gyfc.net.cn/pro_query/' + i)
        return complete_url_list

    def get_build_detail_url(self, build_list_url):
        p = ProducerListUrl(
            current_url_rule='//*[@id="proInfodetail_panResult"]/table/tr/td//table/tr/td[1]/table/tr[1]/td[1]/a/@href',
            analyzer_type='xpath',
            headers=self.headers,
            encode='gbk',
            list_page_url=build_list_url)
        all_build_detail_url = p.get_current_page_url()
        print(all_build_detail_url)
        return all_build_detail_url

    def get_comm_info(self, all_url_list):
        c = Comm(co_index)
        c.co_name = '>楼盘名称.*?auto">(.*?)&nbsp'  # 15个匹配结果
        c.co_id = 'margin: 8px"><a href="http://www\.gyfc\.net\.cn/2_proInfo/LoupanDetail\.aspx\?lpid=(.*?)".*?查看详细'
        c.co_address = '>楼盘地址.*?<td>(.*?)&nbsp'

        data_list = c.to_dict()

        p = ProducerListUrl(list_page_url=all_url_list,
                            request_type='get', encode='gbk',
                            current_url_rule='margin: 8px"><a href="(.*?)".*?查看详细',
                            analyzer_rules_dict=data_list,
                            analyzer_type='regex',
                            headers=self.headers)
        url_list = p.get_details()
        return url_list
