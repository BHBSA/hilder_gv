import requests
from lxml import etree
import re
from retry import retry
import json
from lib.rabbitmq import Rabbit
import yaml

setting = yaml.load(open('config_local.yaml'))


def decode(result, encode):
    """
    html编码
    :param result:
    :param encode:
    :return: html.decode()
    """
    if encode:
        html_content = result.content.decode(encode)
    else:
        html_content = result.content.decode()
    return html_content


def get_html_dom(html_str, ):
    """
    获取html对象
    :param html_str:
    :return: xpath html 对象
    """
    return etree.HTML(html_str)


@retry(tries=3)
def do_request(url, request_type, headers, encode):
    """

    :param url
    :param request_type:'get', 'post'
    :param headers
    :param encode
    :return: html_tree
    """
    try:
        if request_type is 'get':
            result = requests.get(url, headers=headers, )
            html_str = decode(result, encode)
            return html_str
        else:
            # todo post
            pass
    except Exception as e:
        print(e)
        print('连接错误')
        raise


class ProducerListUrl:
    """
    根据列表页获取详情页的url
    """

    def __init__(self, list_page_url, analyzer_rules_dict, current_url_rule=None, encode=None,
                 request_type='get', headers=None, analyzer_type='regex', ):
        """

        :param list_page_url: 必填，列表页url ,必须是数组
        ['www.google.com', 'www.github.com']
        :param analyzer_rules_dict: 必填，解析表达式,必须是数组
        [{'co_build_size': None, 'co_owner': None, 'co_build_type': None, 'co_build_end_time': None, 'co_green': None,}]
        :param current_url_rule: 获取当前页面的url的正则表达式/xpath
        :param encode: 编码方式：get，post
        :param request_type: 默认get,可选get, post
        :param headers: requests header {  'Cache-Control': "no-cache','User-Agent':'safari', }
        :param analyzer_type: 默认未正则表达式
        """
        self.list_page_url = list_page_url
        self.encode = encode
        self.request_type = request_type
        self.headers = headers
        self.analyzer_type = analyzer_type
        self.current_url_rule = current_url_rule
        self.analyzer_rules_dict = analyzer_rules_dict

    def get_list_page_url(self, html_str):
        # 判断解析方式
        url_list = []
        if self.analyzer_type is 'regex':
            # 正则表达式
            print('开始正则表达式获取当前的页面url')
            regex_url_list = re.findall(self.current_url_rule, html_str, re.M | re.S)
            print(len(regex_url_list))
            for url in regex_url_list:
                print(url)
                url_list.append(url)
        else:
            # xpath
            html_tree = get_html_dom(html_str)
            xpath_url_list = html_tree.xpath(self.current_url_rule)
            print(len(xpath_url_list))
            for url in xpath_url_list:
                # print(url)
                url_list.append(url)
        # 解析page_list获取数组返回
        # print(url_list)
        return url_list

    def get_details(self):
        """
        把网页放入队列
        如果有list_page_url，返回url列表
        :return:
        """
        if not isinstance(self.list_page_url, list):
            print('list_url 必须是数组')
            return

        r = Rabbit(host=setting['rabbitmq_host'], port=setting['rabbitmq_port'])
        channel = r.get_channel()
        channel.queue_declare(queue='hilder_gv')
        all_list_page_url = []
        for i in self.list_page_url:
            try:
                html_str = do_request(i, self.request_type, self.headers, self.encode)
                body = {'html': html_str,
                        'analyzer_type': self.analyzer_type,
                        'analyzer_rules_dict': self.analyzer_rules_dict,
                        }
                # 放入队列 json.dumps(body)
                channel.basic_publish(exchange='',
                                      routing_key='hilder_gv',
                                      body=json.dumps(body))
                print(json.dumps(body))
                print('已经放入队列')
                if self.current_url_rule:
                    current_page_list_url = self.get_list_page_url(html_str)
                    all_list_page_url = all_list_page_url + current_page_list_url
            except Exception as e:
                print(i, e)
                continue
        print(all_list_page_url)
        r.get_connection().close()
        return all_list_page_url


if __name__ == '__main__':
    # list_url = ['http://www.czfdc.gov.cn/spf/gs.php']
    while True:
        list_url = ['http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    'http://www.czfdc.gov.cn/spf/gs.php',
                    ]

        from comm_info import Comm

        c = Comm('100')
        c.co_name = '//*[@id="right"]/table/tr/td/div/table/tr/td/table/tr[1]/td[3]'

        data_list = c.to_dict()
        current_url_rule = '//*[@id="right"]/table/tr/td/div/table/tr/td[1]/table/tr[1]/td[1]/a/@href'
        g = ProducerListUrl(list_page_url=list_url, request_type='get', encode='gbk',
                            current_url_rule=current_url_rule,
                            analyzer_rules_dict=data_list, analyzer_type='xpath', )
        g.get_details()
