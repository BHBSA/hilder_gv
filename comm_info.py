"""
小区字段
"""


class Comm:
    def __init__(self, co_index=None, co_name=None, co_id=None, co_address=None, co_type=None, co_green=None,
                 co_is_build=None, co_size=None, co_build_size=None, co_build_start_time=None, co_build_end_time=None,
                 co_investor=None, co_pre_sale=None, co_land_use=None, co_volumetric=None,):
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

    def comm_to_mongo(self):
        pass


if __name__ == '__main__':
    c = Comm()
    c.id = '1100'
    c.name = 'mingzi'
    print(c.name)
    print(c.id)
