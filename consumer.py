import pika
import json
from lxml import etree
import re

class Consumer(object):
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.190', 5673))
    channel = connection.channel()
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
                if i == 'co_index':
                    continue
                info_list = tree.xpath(analyzer_rules_dict[i])
                info[i] = info_list
            pass
            # todo info入库

        elif analyzer_type == 'regex':
            html = html.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
            info = {}
            for i in analyzer_rules_dict:
                if not i:
                    continue
                info_list = re.findall(analyzer_rules_dict[i],html)

                info[i] = info_list
        elif analyzer_type == 'xml':
            tree = etree.XML(html)


        if data_type is 'comm':
            pass
        elif data_type is 'build':
            # todo build
            pass
        elif data_type is 'house':
            # todo house
            pass
        tree = etree.HTML(html)


        ch.basic_ack(delivery_tag=method.delivery_tag)


    def consume_queue(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback,
                                   queue='hilder_gv')

        self.channel.start_consuming()


if __name__ == '__main__':
    consumer = Consumer()
    consumer.consume_queue()
