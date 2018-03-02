"""
url = http://www.gafdc.cn/newhouse/houselist.aspx?hou=0-0-0-0-0-0-&page=1
city : 广安
CO_INDEX : 12
author: 吕三利
小区数量：14页    2018/3/1
"""
from crawler_base import Crawler
from lxml import etree
from comm_info import Comm, Building, House
import requests, re
from producer import ProducerListUrl, do_request
from get_page_num import AllListUrl


class Guangan(Crawler):
    def __init__(self):
        self.url = 'http://www.gafdc.cn/newhouse/houselist.aspx?hou=0-0-0-0-0-0-&page=1'

    def start_crawler(self):
        self.start()

    def start(self):
        b = AllListUrl(first_page_url=self.url,
                       request_method='get',
                       analyzer_type='regex',
                       encode='utf-8',
                       page_count_rule='pg.pageCount = (.*?);',
                       )
        page = b.get_page_count()
        for i in range(1, int(page) + 1):
            all_url = 'http://www.gafdc.cn/newhouse/houselist.aspx?hou=0-0-0-0-0-0-&page=' + str(i)
            response = requests.get(all_url)
            html = response.text
            tree = etree.HTML(html)
            comm_detail_list = tree.xpath('//div[@class="newexleft"]/div/ul[2]/li[1]/a/@href')
            for i in comm_detail_list:
                c = Comm(12)
                i = i.replace('index', 'base')
                comm_url = 'http://www.gafdc.cn/newhouse/' + i
                c.co_id = re.search('id=(.*?)$', comm_url).group(1)
                c.co_address = '//div[@class="Detailsleft"]/ul[3]/li[2]/text()'
                c.co_develops = '//div[@class="Detailsleft"]/ul[10]/li[2]/text()'
                c.co_pre_sale = '//div[@class="Detailsleft"]/ul[12]/li[2]/text()'
                c.co_name = '//*[@id="divbody"]/div[5]/ul[1]/li[1]/text()'
                data_list = c.to_dict()
                p = ProducerListUrl(list_page_url=[comm_url], request_type='get', encode='utf-8',
                                    analyzer_rules_dict=data_list, analyzer_type='xpath',
                                    current_url_rule='//div[@class="houbanner"]/a[4]/@href')
                build_url_list = p.get_details()
                for i in build_url_list:
                    b = Building('12')
                    url = 'http://www.gafdc.cn/newhouse/' + i
                    b.bu_all_house = '//*[@class="font12black-center"]/td[2]/text()'
                    b.co_id = c.co_id
                    b.bu_id = '//*[@class="font12black-center"]/td[5]/text()'
                    b.bu_pre_sale = '//*[@class="font12black-center"]/td[1]/text()'
                    p = ProducerListUrl(list_page_url=[comm_url], request_type='get', encode='utf-8',
                                        analyzer_rules_dict=data_list, analyzer_type='xpath',
                                        current_url_rule='//*[@class="font12black-center"]/td[6]/a/@onclick')
                    house_url_list = p.get_details()
                    for i in house_url_list:
                        itemRecord = re.search("\('(.*?)'", i).group(1)
                        houseCode = re.search("'(.*?)'\)", i).group(1)
                        # floor = self.get_floor(itemRecord, houseCode)
                        floor = self.get_house_info(itemRecord, houseCode)

    def get_house_info(self, itemRecord, houseCode):
        url = 'http://www.gafdc.cn/newhouse/GetBuildTableByAjax.ashx'
        data = {
            'itemRecord': itemRecord,
            'houseCode': houseCode,
        }
        response = requests.post(url=url, data=data)
        html = response.text
        tree = etree.XML(html)
        house_info_list = tree.xpath('//td[@class="border-333333"]/text()')
        house_info_list = tree.xpath('//td[@class="border-333333"]/@Title')

# def get_floor(self, itemRecord, houseCode):
#     url = 'http://www.gafdc.cn/newhouse/GetBuildTableByAjax.ashx'
#     data = {
#         'itemRecord': itemRecord,
#         'houseCode': houseCode,
#     }
#     response = requests.post(url=url, data=data)
#     html = response.text
#     tree = etree.XML(html)
#     floor = tree.xpath('//td[@class="border-F9D6BA"]/text()')[0].strip()
#     return floor

# result = requests.get(comm_url)
# html = result.text
# tree = etree.HTML(html)
# comm_detail_url = tree.xpath('//div[@class="houbanner"]/a[2]/@href')[0]
# url = 'http://www.gafdc.cn/newhouse/' + comm_detail_url
# response = requests.get(url=url)
# html = response.text
# tree = etree.HTML(html)













# for i in comm_url_list:
#     url = 'http://www.gafdc.cn/newhouse/'+i
#     p = ProducerListUrl(list_page_url=list_page_url, request_type='get', encode='utf-8',
#                         analyzer_rules_dict=None, analyzer_type='xpath',
#                         current_url_rule='//div[@class="houbanner"]/a[2]/@href')
#     html = do_request(url, 'get', None, 'utf-8')
#     comm_detail = p.get_list_page_url(html)[0]
#     comm_url = 'http://www.gafdc.cn/newhouse/' + comm_detail
#     c = Comm('12')
#     c.co_address = '//div[@class="Detailsleft"]/ul[3]/li[2]/text()'
#     c.co_develops = '//div[@class="Detailsleft"]/ul[10]/li[2]/text()'
#     data_t = c.data_type
#     data_list = c.to_dict()
#     pass
