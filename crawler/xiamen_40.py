"""
url = http://fdc.xmtfj.gov.cn:8001/search/commercial_property
city :  厦门
CO_INDEX : 40
author: 程纪文
"""

from crawler_base import Crawler
from comm_info import Comm
import re, requests
import json

co_index = 40


class Xiamen(Crawler):
    def __init__(self):
        self.start_url = "http://fdc.xmtfj.gov.cn:8001/search/commercial_property"
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
        }

    def start_crawler(self):
        co = Comm(co_index)
        for i in range(1, 10000):
            try:
                formdata = {
                    "currentpage": i,
                    "pagesize": 20,
                }
                res = requests.post("http://fdc.xmtfj.gov.cn:8001/home/Getzslp", data=formdata, headers=self.headers)
                con = json.loads(res.text)
                con = str(con)
                co_name = re.findall('"XMMC":"(.*?)"', con)
                co_id = re.findall('"TRANSACTION_ID":"(.*?)"', con)
                co_address = re.findall('"XMDZ":"(.*?)"', con)
                co_pre_sale = re.findall('"YSXKZH":"(\d+)"', con)
                co_all_house = re.findall('"PZTS":(\d+)', con)
                co_build_size = re.findall('"PZMJ":(\d+)', con)
                co_area = re.findall('"XMDQ":"(.*?)"', con)
                co_pre_date = re.findall('"GETDATE":"(.*?)"', con)
                if len(co_name) == 0:
                    break
                else:
                    for index in range(1, len(co_name) + 1):
                        co.co_name = co_name[index]
                        co.co_id = co_id[index]
                        co.co_address = co_address[index]
                        co.co_pre_sale_date = co_pre_date[index]
                        co.co_pre_sale = co_pre_sale[index]
                        co.area = co_area[index]
                        co.co_build_size = co_build_size[index]
                        co.co_all_house = co_all_house[index]

                        co.insert_db()
            except:
                continue


if __name__ == '__main__':
    xiamen = Xiamen()
    xiamen.start_crawler()
