"""
url = 'http://hkrealestate.haikou.gov.cn/?page_id=1463'
co_index :14
海口
程纪文
"""

from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import re, requests
from lxml import etree
import json

co_index = "14"
city = "海口"
class Haikou(Crawler):
    def __init__(self):
        self.headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Cookie': 'PHPSESSID=sq4asdaq5bmeqjdrs3n4a71h1h; slimstat_tracking_code=741072.767f13385e08aafb4619510f78034160',
            'Referer': 'http://hkrealestate.haikou.gov.cn/wp_myself/housequery/queryProjectInfo.php',
            'Postman-Token': "c67c04c6-f1e2-44aa-bd0b-d6560456a17b"
        }
        self.start_url = 'http://hkrealestate.haikou.gov.cn/wp_myself/housequery/queryProjectInfo.php'
        self.formdata = {"action":"queryProjectLists","webUrl":'1'}
        self.url='http://hkrealestate.haikou.gov.cn/wp_myself/housequery/projectBuildHouseAction.php'

    def start_crawler(self):
        m = requests.session()

        m.get('http://hkrealestate.haikou.gov.cn/')
        # print(s.cookies)

        url = "http://hkrealestate.haikou.gov.cn/wp_myself/housequery/projectBuildHouseAction.php"
        for i in range(1, 62):
            page = str(i)
            payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\nqueryProjectLists\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"page\"\r\n\r\n" + page + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"pk\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"num\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"webUrl\"\r\n\r\n5\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
            headers = {
                'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
                'Referer': "http://hkrealestate.haikou.gov.cn/wp_myself/housequery/queryProjectInfo.php",
                'Cache-Control': "no-cache",
                'Postman-Token': "c57f57a2-32aa-2739-ff2c-77c7e078bcdc"
            }

            res = m.request("POST", url, data=payload, headers=headers)
            # print(response.text)
            k = re.findall("onclick=\"doview\(('\d+','.*?')\)",res.text,re.S|re.M)
            for n in k:
                formdata = {}
                ret = re.split(',',n)
                co_id = formdata["pk"] = ret[0].strip("\\'")
                num = ret[1].strip("'")
                s = str(i)
                load = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\nqueryProjectLists\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"page\"\r\n\r\n" + page + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"pk\"\r\n\r\n" + co_id + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"num\"\r\n\r\n" + num + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"webUrl\"\r\n\r\n" + s + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data;------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\nqueryProjectLists\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"page\"\r\n\r\n" + page + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"pk\"\r\n\r\n" + co_id + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"num\"\r\n\r\n" + num + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"webUrl\"\r\n\r\n" + s + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data;"
                comm_res = m.request("POST", url, data=load, headers=headers)
                self.get_comm_info(comm_res,co_id)


    def get_comm_info(self,comm_res,co_id):
        comm = Comm(co_index)
        con = comm_res.text
        comm.co_name = re.search('项目名称.*?">(.*?)&nbsp',con,re.S|re.M).group(1)
        comm.co_id = co_id
        comm.co_address = re.search('项目地址.*?<td>(.*?)&nbsp',con,re.S|re.M).group(1)
        comm.co_develops = re.search('开发商.*?">(.*?)&nbs',con,re.S|re.M).group(1)
        comm.co_all_size = re.search('建设用地面积.*?<td>(.*?)</td>',con,re.S|re.M).group(1)
        comm.co_size = re.search('占地面积.*?<td>(.*?)</td>',con,re.S|re.M).group(1)
        comm.co_land_use = re.search('建筑面积.*?<td>(.*?)</td>',con,re.S|re.M).group(1)
        comm.co_plan_pro = re.search('土地使用证号.*?<td>(.*?)&nbsp',con,re.S|re.M).group(1)
        comm.co_build_size = re.search('规划许可证号.*?<td>(.*?)&nbsp',con,re.S|re.M).group(1)
        comm.insert_db()

        build_id_list = re.findall("onclick=\"doview\('(\d+)'\)\"",con,re.S|re.M)
        self.get_build_info(build_id_list,co_id)

    def get_build_info(self,build_id_list,co_id):
        bu = Building(co_index)
        for build_id in build_id_list:
            formdata={}
            formdata["action"] = "queryProjectLists"
            formdata['pk'] = str(build_id)
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
                "Cookie":"PHPSESSID=sq4asdaq5bmeqjdrs3n4a71h1h; slimstat_tracking_code=740908.ec611c5b4de58f4104826de4ed88392e",
                'Referer':'http://hkrealestate.haikou.gov.cn/wp_myself/housequery/projectBuildingList.php'
            }
            build_info = requests.post(self.url,data=formdata,headers=header)

            build_con = build_info.text
            bu.bu_id = build_id
            bu.co_id =co_id
            bu.bu_num = re.search('幢名称.*?<td>(.*?)&nbsp',build_con,re.S|re.M).group(1)
            bu.bu_floor = re.search('总层数.*?<td>(.*?)&nbsp',build_con,re.S|re.M).group(1)
            bu.bu_build_size = re.search('>建筑面积.*?<td>(.*?)&nbsp',build_con,re.S|re.M).group(1)
            bu.bo_develops = re.search('房地产企业.*?">(.*?)&nbsp;</td',build_con,re.S|re.M).group(1)

            bu.insert_db()

            self.get_house_info(build_con,co_id,build_id)

    def get_house_info(self,con,co_id,build_id):
        ho = House(co_index)

        ho_num = re.findall("HC_HOUSENUMB':",con,re.S|re.M)
        ho_roomtype = re.findall("HC_HOUSETYPE':",con,re.S|re.M)
        ho_buid_size = re.findall("HC_STCTAREA':",con,re.S|re.M)
        ho_type = re.findall("HC_BLDUSAGE':",con,re.S|re.M)
        for index in range(len(ho_num)+1):
            ho.co_id = co_id
            ho.bu_id = build_id
            ho.ho_num = ho_num[index]
            ho.ho_room_type = ho_roomtype[index]
            ho.ho_build_size = ho_buid_size[index]
            ho.ho_type = ho_type[index]

            ho.insert_db()

