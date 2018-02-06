"""
Comm :小区字段
Building:楼栋和房号字段
House:房屋类型
"""
from lib.mongo import Mongo
import datetime


def serialization_info(info):
    """

    :param comm_info:
    :return: data:
    """
    data = {}
    for key, value in vars(info).items():
        if key is 'coll':
            continue
        data[key] = value
    return data


class Comm:
    def __init__(self, co_index=None, co_name=None, co_id=None, co_address=None, co_type=None, co_green=None,
                 co_is_build=None, co_size=None, co_build_size=None, co_build_start_time=None, co_build_end_time=None,
                 co_investor=None, co_pre_sale=None, co_land_use=None, co_volumetric=None, ):
        self.co_index = co_index  # 网站id
        self.co_name = co_name  # 小区名称
        self.co_id = co_id  # 小区id
        self.co_address = co_address  # 小区地址
        self.co_type = co_type  # 小区类型 :商品房
        self.co_green = co_green  # 绿化率
        self.co_is_build = co_is_build  # 竣工/是否在建 1 已经完成/竣工 0未完成/正在建立
        self.co_size = co_size  # 占地面的
        self.co_build_size = co_build_size  # 建筑面积
        self.co_build_start_time = co_build_start_time  # 开工时间
        self.co_build_end_time = co_build_end_time  # 竣工时间
        self.co_investor = co_investor  # 投资商
        self.co_pre_sale = co_pre_sale  # 预售证书
        self.co_land_use = co_land_use  # 土地使用证
        self.co_volumetric = co_volumetric  # 容积率

        self.time = datetime.datetime.now()
        self.coll = Mongo('192.168.0.235', 27017, 'gv', 'community').get_collection_object()

    def insert_db(self):
        data = serialization_info(self)
        print(data)
        self.coll.insert_one(data)


class Building:
    def __init__(self, co_index=None, co_id=None, bu_num=None, bu_all_house=None, bu_floor=None, bu_build_size=None,
                 bu_live_size=None, bu_not_live_size=None, bu_price=None):
        self.co_index = co_index  # 网站id
        self.co_id = co_id  # 小区id

        self.bu_num = bu_num  # 楼号 栋号
        self.bu_all_house = bu_all_house  # 总套数
        self.bu_floor = bu_floor  # 楼层

        self.bu_build_size = bu_build_size  # 建筑面积
        self.bu_live_size = bu_live_size  # 住宅面积
        self.bu_not_live_size = bu_not_live_size  # 非住宅面积

        self.bu_price = bu_price  # 住宅价格

        self.time = datetime.datetime.now()
        self.coll = Mongo('192.168.0.235', 27017, 'gv', 'building').get_collection_object()

    def insert_db(self):
        data = serialization_info(self)
        print(data)
        self.coll.insert_one(data)


class House:
    def __init__(self):
        self.time = datetime.datetime.now()
        self.coll = Mongo('192.168.0.235', 27017, 'gv', 'house').get_collection_object()


if __name__ == '__main__':
    c = Comm()
    c.co_index = '1100'
    c.co_name = 'mingzi'
    c.insert_db()
