from flask import Flask
from flask import request
from flask import render_template
from pymongo import MongoClient
import city_dict
import json

app = Flask(__name__)
client = MongoClient('192.168.0.235', 27017)
db = client['gv']


@app.route("/", methods=['POST', 'GET'])
def query():
    if request.method == 'GET':
        return render_template('hello.html')
    city = request.form['city']
    print(city)
    co_index = city_dict.city_index[city]
    print(co_index)
    comm_collection = db['community']
    build_collection = db['building']
    house_collection = db['house']

    city_count = comm_collection.find({'co_index': int(co_index)}).count()
    bu_count = build_collection.find({'co_index': int(co_index)}).count()
    house_count = house_collection.find({'co_index': int(co_index)}).count()
    city = city_dict.dict_city[co_index]
    print('城市:' + city + ', 小区:' + str(city_count) + ', 楼栋:' + str(bu_count) + ', 房号:' + str(house_count))
    count_dict = {
        '城市': city,
        '小区': str(city_count),
        '楼栋': str(bu_count),
        '房号': str(house_count),
    }

    return render_template('hello.html', count_dict=count_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
