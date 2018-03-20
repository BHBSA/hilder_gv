from flask import Flask
from pymongo import MongoClient
import city_dict
import json

app = Flask(__name__)
client = MongoClient('192.168.0.235', 27017)
db = client['gv']


@app.route("/")
def hello():
    comm_collection = db['community']
    build_collection = db['building']
    house_collection = db['house']
    json_array = []
    print('开始查询')
    for i in city_dict.dict_city:
        city_count = comm_collection.find({'co_index': int(i)}).count()
        bu_count = build_collection.find({'co_index': int(i)}).count()
        house_count = house_collection.find({'co_index': int(i)}).count()
        city = city_dict.dict_city[i]
        print('城市:' + city + ', 小区:' + str(city_count) + ', 楼栋:' + str(bu_count) + ', 房号:' + str(house_count))
        json_array.append({
            '城市': city,
            '小区': str(city_count),
            '楼栋': str(bu_count),
            '房号': str(house_count),
        })
        break
    return str(json_array)


if __name__ == '__main__':
    app.run()
