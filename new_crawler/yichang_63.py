"""
url = http://www.ycfcjy.com
city :  宜昌
CO_INDEX : 63
author: 程纪文
"""

from crawler_base import Crawler
from comm_info import Comm, Building, House
from get_page_num import AllListUrl
from producer import ProducerListUrl
import re, requests
from lxml import etree
import json
from multiprocessing import Process,Queue
co_index = 63

class Yichang(Crawler):
    def __init__(self):
        self.start_url = "http://www.ycfcjy.com"
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36', }
    def start_crawler(self):
        url =  self.start_url+"/api/buildInfos/pageHousePreSales?page=1&limit=10000&state=2&code=1"
        res = requests.get(url,headers=self.headers)
        dict = json.loads(res.text)
        data  = dict["data"]["data"]

        for i in data:
            id = i["blockNumber"]
            self.comm(id)

    def comm(self,id):
        # co = Comm(co_index)
        bu = Building(co_index)

        house_url = self.start_url +"/api/buildInfos/getHouseInfosByPannelNumber?pannelNumber="+str(id)
        comm_url = self.start_url +"/api/buildInfos/getHomePageBuildingInfo?blockNumber=" +str(id)
        comm_detail_url = self.start_url + "/api/buildInfos/getDetailsBuildingInfo?blockNumber=" + str(id)

        comm_res = requests.get(comm_url)
        comm_detail_res = requests.get(comm_detail_url)
        house_res = requests.get(house_url)
        comm_dict = json.loads(comm_res.text)
        comm_detail_dict = json.loads(comm_detail_res.text)
        house_dict = json.loads(house_res.text)

        # co.co_id = id
        # co.co_name = comm_dict["data"]["nameBuildings"]
        # co.co_build_size = comm_dict["data"]["barea"]
        # co.co_size = comm_dict["data"]["eartharea"]
        # co.co_develops = comm_dict["data"]["companyName"]
        # co.co_address = comm_dict["data"]["houseaddress"]
        # co.co_type = comm_dict["data"]["propertycategory"]
        # co.co_build_type = comm_detail_dict["data"]["buildcategory"]
        # co.co_green = comm_detail_dict["data"]["greenRate"]
        # co.co_volumetric = comm_detail_dict["data"]["plotRatio"]
        # co.area = comm_detail_dict["data"]["houseingArea"]
        # co.co_pre_sale = comm_detail_dict["data"]["yszh"]
        # co.co_plan_pro = comm_detail_dict["data"]["plytnum"]
        # co.co_work_pro = comm_detail_dict["data"]["cnsnum"]
        # co.co_handed_time = comm_detail_dict["data"]["checkintime"]
        # co.co_all_house = comm_detail_dict["data"]["totalrooms"]
        # co.insert_db()

        bu.bu_id = id
        bu.bu_num = comm_dict["data"]["nameBuildings"]
        bu.bu_address = comm_dict["data"]["houseaddress"]
        bu.bu_pre_sale = comm_detail_dict["data"]["yszh"]
        bu.bu_type = comm_dict["data"]["propertycategory"]
        bu.bo_develops = comm_dict["data"]["companyName"]
        bu.insert_db()

        house_num = house_dict["data"]
        for hu in house_num:
            ho = House(co_index)
            h = hu["data"]
            if len(h)>0:
                for i in h:
                    room_id = i["houseNumber"]
                    room_url = self.start_url + "/api/buildInfos/getHouseInfoByHouseNumber?houseNumber=" +str(room_id)
                    res = requests.get(room_url,headers=self.headers)
                    dict = json.loads(res.text)
                    ho.bu_id = id
                    ho.ho_num = room_id
                    ho.ho_name = dict["data"]["houseNo"]
                    ho.ho_build_size = dict["data"]["buildArea"]
                    ho.ho_true_size = dict["data"]["jacketArea"]
                    ho.ho_share_size = dict["data"]["apportionedArea"]
                    ho.ho_floor = dict["data"]["nominalLevel"]
                    ho.insert_db()
            else:
                continue



