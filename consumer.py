import json
from lxml import etree
import re
from comm_info import Comm, Building, House
import yaml

setting = yaml.load(open('config_local.yaml'))
from lib.rabbitmq import Rabbit


class Consumer(object):
    r = Rabbit(host=setting['rabbitmq_host'], port=setting['rabbitmq_port'])
    channel = r.get_channel()
    channel.queue_declare(queue='hilder_gv')

    def callback(self, ch, method, properties, body):
        body = json.loads(body.decode())
        analyzer_rules_dict = body['analyzer_rules_dict']
        co_index = analyzer_rules_dict['co_index']
        data_type = analyzer_rules_dict['data_type']
        analyzer_type = body['analyzer_type']
        html = body['html']
        if analyzer_type == 'xpath':
            tree = etree.HTML(html)
            info = {}
            for i in analyzer_rules_dict:
                if not analyzer_rules_dict[i]:
                    continue
                if i == 'co_index' or i == 'data_type':
                    continue
                info_list = tree.xpath(analyzer_rules_dict[i])
                if info_list:
                    info[i] = info_list
            if not info:
                print('\n\n没有获得任何信息\n\n')
            self.put_database(info, data_type, co_index)
        elif analyzer_type == 'regex':
            info = {}
            for i in analyzer_rules_dict:
                if not analyzer_rules_dict[i]:
                    continue
                if i == 'co_index' or i == 'data_type':
                    continue
                info_list = re.findall(analyzer_rules_dict[i], html, re.M | re.S)
                if info_list:
                    info[i] = info_list
            if not info:
                print('\n\n没有获得任何信息\n\n')
            self.put_database(info, data_type, co_index)

        elif analyzer_type == 'xml':
            tree = etree.XML(html)
            info = {}
            for i in analyzer_rules_dict:
                if not analyzer_rules_dict[i]:
                    continue
                if i == 'co_index' or i == 'data_type':
                    continue
                info_list = tree.xpath(analyzer_rules_dict[i])
                if info_list:
                    info[i] = info_list
            if not info:
                print('\n\n没有获得任何信息\n\n')
            self.put_database(info, data_type, co_index)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 遍历字典放入数据库
    def put_database(self, info, data_type, co_index):
        key = sorted(info.items())[0][0]
        length = len(info[key])
        for i in range(0, length):
            obj = self.get_data_obj(data_type, co_index)
            for key, value in info.items():
                if value:
                    setattr(obj, key, value[i].strip())
            obj.insert_db()

    # 创建对象（data_type是什么类型是就创建什么对象）
    def get_data_obj(self, data_type, co_index):
        if data_type == 'comm':
            return Comm(co_index)
        elif data_type == 'build':
            return Building(co_index)
        elif data_type == 'house':
            return House(co_index)

    def consume_queue(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback, queue='hilder_gv')
        self.channel.start_consuming()


if __name__ == '__main__':
    consumer = Consumer()
    consumer.consume_queue()
