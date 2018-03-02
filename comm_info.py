"""
Comm :小区字段
Building:楼栋和房号字段
House:房屋类型
"""
from lib.mongo import Mongo
import datetime
import yaml

setting = yaml.load(open('config_local.yaml'))


def serialization_info(info):
    """

    :param info:
    :return: data:
    """
    data = {}
    for key, value in vars(info).items():
        if key is 'coll':
            continue
        data[key] = value
    return data


class Comm:
    def __init__(self, co_index, co_name=None, co_id=None, co_address=None, co_type=None, co_green=None,
                 co_is_build=None, co_size=None, co_build_size=None, co_build_start_time=None, co_build_end_time=None,
                 co_investor=None, co_pre_sale=None, co_land_use=None, co_volumetric=None, co_owner=None,
                 co_build_type=None, co_build_structural=None, co_pre_sale_date=None, co_develops=None,
                 co_open_time=None, co_handed_time=None, co_all_house=None, data_type='comm'):
        self.co_index = int(co_index)  # 网站id
        self.co_name = co_name  # 小区名称
        self.co_id = co_id  # 小区id
        self.co_address = co_address  # 小区地址
        self.co_type = co_type  # 小区类型/物业类型 :商品房/商品房/别墅
        self.co_build_type = co_build_type  # 建筑类型:独栋,小高层,高层多层
        self.co_green = co_green  # 绿化率
        self.co_is_build = co_is_build  # 竣工/是否在建 1 已经完成/竣工 0未完成/正在建立
        self.co_size = co_size  # 占地面的
        self.co_build_size = co_build_size  # 建筑面积
        self.co_build_start_time = co_build_start_time  # 开工时间
        self.co_build_end_time = co_build_end_time  # 竣工时间
        self.co_investor = co_investor  # 投资商
        self.co_develops = co_develops  # 开发商
        self.co_pre_sale = co_pre_sale  # 预售证书
        self.co_pre_sale_date = co_pre_sale_date  # 预售证书日期
        self.co_open_time = co_open_time  # 小区开盘时间
        self.co_handed_time = co_handed_time  # 小区交房时间
        self.co_all_house = co_all_house  # 小区总套数
        self.co_land_use = co_land_use  # 土地使用证
        self.co_volumetric = co_volumetric  # 容积率
        self.co_owner = co_owner  # 房产证/房屋所有权证
        self.co_build_structural = co_build_structural  # 建筑结构：钢筋混泥土

        # self.time = datetime.datetime.now()
        self.data_type = data_type
        self.coll = Mongo(setting['db'], setting['port'], setting['db_name'],
                          setting['coll_comm']).get_collection_object()

    def to_dict(self):
        data = serialization_info(self)
        return data

    def insert_db(self):
        data = serialization_info(self)
        print(data)
        self.coll.insert_one(data)


class Building:
    def __init__(self, co_index, co_id=None, bu_num=None, bu_id=None, bu_all_house=None,
                 bu_floor=None, bu_build_size=None, bu_live_size=None, bu_not_live_size=None, bu_price=None,
                 bu_pre_sale=None, bu_pre_sale_date=None, co_name=None, data_type='build', size=None, bo_develops=None,
                 bo_build_start_time=None, bo_build_end_time=None):
        self.co_index = int(co_index)  # 网站id
        self.co_id = co_id  # 小区id
        self.co_name = co_name  # 小区名称
        self.bu_id = bu_id  # 楼栋id
        self.bu_num = bu_num  # 楼号 栋号
        self.bu_all_house = bu_all_house  # 总套数
        self.bu_floor = bu_floor  # 楼层
        self.size = size  # 占地面积
        self.bu_build_size = bu_build_size  # 建筑面积
        self.bu_live_size = bu_live_size  # 住宅面积
        self.bu_not_live_size = bu_not_live_size  # 非住宅面积
        self.bu_price = bu_price  # 住宅价格
        self.bu_pre_sale = bu_pre_sale  # 楼栋预售证书
        self.bu_pre_sale_date = bu_pre_sale_date  # 楼栋预售证书日期
        self.bo_develops = bo_develops  # 开发商
        self.bo_build_start_time = bo_build_start_time  # 开工时间
        self.bo_build_end_time = bo_build_end_time  # 竣工时间

        # self.time = datetime.datetime.now()
        self.data_type = data_type
        self.coll = Mongo(setting['db'], setting['port'], setting['db_name'],
                          setting['building']).get_collection_object()

    def to_dict(self):
        data = serialization_info(self)
        return data

    def insert_db(self):
        data = serialization_info(self)
        print(data)
        self.coll.insert_one(data)


class House:
    def __init__(self, co_index, co_id=None, bu_id=None, bu_num=None, ho_num=None, ho_floor=None, ho_type=None,
                 ho_room_type=None, ho_build_size=None, ho_true_size=None, ho_share_size=None, ho_price=None,
                 orientation=None, ho_name=None, data_type='house', info=None):
        self.co_index = int(co_index)  # 网站id
        self.bu_num = bu_num  # 楼号 栋号
        self.co_id = co_id  # 小区id
        self.bu_id = bu_id  # 楼栋id
        self.ho_name = ho_name  # 房号：3单元403
        self.ho_num = ho_num  # 房号id
        self.ho_floor = ho_floor  # 楼层
        self.ho_type = ho_type  # 房屋类型：普通住宅 / 车库仓库
        self.ho_room_type = ho_room_type  # 户型：一室一厅
        self.ho_build_size = ho_build_size  # 建筑面积
        self.ho_true_size = ho_true_size  # 预测套内面积,实际面积
        self.ho_share_size = ho_share_size  # 分摊面积
        self.ho_price = ho_price  # 价格
        self.orientation = orientation  # 朝向
        self.info = info  # 无法判断是什么的数据

        # self.time = datetime.datetime.now()
        self.data_type = data_type
        self.coll = Mongo(setting['db'], setting['port'], setting['db_name'], setting['house']).get_collection_object()

    def to_dict(self):
        data = serialization_info(self)
        return data

    def insert_db(self):
        data = serialization_info(self)
        print(data)
        self.coll.insert_one(data)


if __name__ == '__main__':
    c = Comm('1100')
    c.co_name = 'mingzi'
    c.insert_db()
