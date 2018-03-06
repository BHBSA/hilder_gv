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
        analyzer_type = body['analyzer_type']
        for analyzer in analyzer_rules_dict:
            co_index = analyzer_rules_dict[analyzer]['co_index']
            html = body['html']
            if analyzer == 'comm':
                if analyzer_type == 'regex':
                    info = {}
                    for i in analyzer_rules_dict[analyzer]:
                        if not analyzer_rules_dict[analyzer][i]:
                            continue
                        if i == 'co_index' or i == 'data_type':
                            continue
                        info_list = re.findall(analyzer_rules_dict[analyzer][i], html, re.M | re.S)
                        if info_list:
                            info[i] = info_list
                    if not info:
                        print('\n\n没有获得任何信息\n\n')
                        continue
                    self.put_database(info, analyzer, co_index)
                elif analyzer_type == 'xpath':
                    tree = etree.HTML(html)
                    info = {}
                    for i in analyzer_rules_dict[analyzer]:
                        if not analyzer_rules_dict[analyzer][i]:
                            continue
                        if i == 'co_index' or i == 'data_type':
                            continue
                        info_list = tree.xpath(analyzer_rules_dict[analyzer][i])
                        if info_list:
                            info[i] = info_list
                    if not info:
                        print('\n\n没有获得任何信息\n\n')
                        continue
                    self.put_database(info, analyzer, co_index)
                elif analyzer_type == 'xml':
                    pass
            elif analyzer == 'build':
                if analyzer_type == 'regex':
                    info = {}
                    co_id = re.findall(analyzer_rules_dict[analyzer]['co_id'], html, re.M | re.S)
                    co_name = re.findall(analyzer_rules_dict[analyzer]['co_name'], html, re.M | re.S)
                    if co_id:
                        co_id = co_id[0]
                    if co_name:
                        co_name = co_name[0]
                    for i in analyzer_rules_dict[analyzer]:
                        if not analyzer_rules_dict[analyzer][i]:
                            continue
                        if i == 'co_index' or i == 'data_type' or i == 'co_id':
                            continue
                        info_list = re.findall(analyzer_rules_dict[analyzer][i], html, re.M | re.S)
                        if info_list:
                            info[i] = info_list
                    if not info:
                        print('\n\n没有获得任何信息\n\n')
                        continue
                    self.put_database(info, analyzer, co_index, co_id, co_name)
                elif analyzer == 'xpath':
                    tree = etree.HTML(html)
                    info = {}
                    co_id = tree.xpath(analyzer_rules_dict[analyzer]['co_id'])
                    co_name = tree.xpath(analyzer_rules_dict[analyzer]['co_name'])
                    if co_id:
                        co_id = co_id[0]
                    if co_name:
                        co_name = co_name[0]
                    for i in analyzer_rules_dict[analyzer]:
                        if not analyzer_rules_dict[analyzer][i]:
                            continue
                        if i == 'co_index' or i == 'data_type' or i == 'co_id':
                            continue
                        info_list = tree.xpath(analyzer_rules_dict[analyzer][i])
                        if info_list:
                            info[i] = info_list
                    if not info:
                        print('\n\n没有获得任何信息\n\n')
                        continue
                    self.put_database(info, analyzer, co_index, co_id, co_name)
                elif analyzer_type == 'xml':
                    pass

            elif analyzer == 'house':
                if analyzer_type == 'regex':
                    info = {}
                    bu_id = re.findall(analyzer_rules_dict[analyzer]['bu_id'], html, re.M | re.S)
                    bu_num = re.findall(analyzer_rules_dict[analyzer]['bu_num'], html, re.M | re.S)
                    if bu_id:
                        bu_id = bu_id[0]
                    if bu_num:
                        bu_num = bu_num[0]
                    info.bu_id = analyzer_rules_dict[analyzer]['bu_id']
                    for i in analyzer_rules_dict[analyzer]:
                        if not analyzer_rules_dict[analyzer][i]:
                            continue
                        if i == 'co_index' or i == 'data_type' or i == 'bu_id':
                            continue
                        info_list = re.findall(analyzer_rules_dict[analyzer][i], html, re.M | re.S)
                        if info_list:
                            info[i] = info_list
                    if not info:
                        print('\n\n没有获得任何信息\n\n')
                        continue
                    self.put_database(info, analyzer, co_index, bu_id, bu_num)
                elif analyzer_type == 'xpath':
                    tree = etree.HTML(html)
                    info = {}
                    bu_id = tree.xpath(analyzer_rules_dict[analyzer]['bu_id'])
                    bu_num = tree.xpath(analyzer_rules_dict[analyzer]['bu_num'])
                    if bu_id:
                        bu_id = bu_id[0]
                    if bu_num:
                        bu_num = bu_num[0]
                    for i in analyzer_rules_dict[analyzer]:
                        if not analyzer_rules_dict[analyzer][i]:
                            continue
                        if i == 'co_index' or i == 'data_type' or i == 'bu_id':
                            continue
                        info_list = tree.xpath(analyzer_rules_dict[analyzer][i])
                        if info_list:
                            info[i] = info_list
                    if not info:
                        print('\n\n没有获得任何信息\n\n')
                        continue
                    self.put_database(info, analyzer, co_index, bu_id, bu_num)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 遍历字典放入数据库
    def put_database(self, info, analyzer, co_index, bu_id=None, bu_num=None, co_id=None, co_name=None):
        key = sorted(info.items())[0][0]
        length = len(info[key])
        for i in range(0, length):
            obj = self.get_data_obj(analyzer, co_index)
            if analyzer == 'comm':
                for key, value in info.items():
                    if value:
                        setattr(obj, key, value[i].strip())
                obj.insert_db()
            elif analyzer == 'build':
                for key, value in info.items():
                    setattr(obj, 'co_id', co_id.strip())
                    setattr(obj, 'co_name', co_name.strip())
                    if value:
                        setattr(obj, key, value[i].strip())
                obj.update_db()
            elif analyzer == 'house':
                for key, value in info.items():
                    setattr(obj, 'bu_id', bu_id.strip())
                    setattr(obj, 'bu_num', bu_num.strip())
                    if value:
                        setattr(obj, key, value[i].strip())
                obj.update_db()

    # 创建对象（data_type是什么类型是就创建什么对象）
    def get_data_obj(self, analyzer, co_index):
        if analyzer == 'comm':
            return Comm(co_index)
        elif analyzer == 'build':
            return Building(co_index)
        elif analyzer == 'house':
            return House(co_index)

    def consume_queue(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback, queue='hilder_gv')
        self.channel.start_consuming()


if __name__ == '__main__':
    consumer = Consumer()
    consumer.consume_queue()
