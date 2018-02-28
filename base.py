import requests
from lxml import etree
import re
from retry import retry


def decode(result, encode):
    if encode:
        html_content = result.content.decode(encode)
    else:
        html_content = result.content.decode()
    return html_content


def do_request(url, method, headers, analyzer, encode):
    """

    :param url:
    :param method:'get', 'post'
    :return: html_tree
    """
    if method is 'get':
        result = requests.get(url, headers=headers)
        if analyzer is 'xpath':
            html_tree = decode(result, encode)
            return etree.HTML(html_tree)
        else:
            html_tree = decode(result, encode)
            return html_tree
    else:
        # todo post
        pass


class AllListUrl:
    """
    根据首页获取全部页数
    :return int(page_num)
    """

    def __init__(self, first_page_url=None, encode=None, request_method=None, headers=None,
                 analyzer='regex', **kwargs):
        """

        :param first_page_url:
        :param method: 'get', 'post'
        :param encode:
        :param kwargs: {'page': page_regex,
        :param kwargs: default regex, you can user xpath either
        """
        self.first_page_url = first_page_url
        self.encode = encode
        self.kwargs = kwargs
        self.method = request_method
        self.analyzer = analyzer
        self.headers = headers

    def get_page_count(self, ):
        html_ = do_request(self.first_page_url, self.method, self.headers, self.analyzer, self.encode)
        if self.analyzer is 'xpath':
            print('开始xpath')
            page_xpath = self.kwargs.get('xpath')
            result = html_.xpath(page_xpath)[0]
            print(int(result.text))
            return int(result.text)
        else:
            print('开始正则')
            page_regex = self.kwargs.get('regex')
            group_regex = self.kwargs.get('regex_group')
            result = re.search(page_regex, html_, re.M | re.S).group(group_regex)
            print(int(result))
            return int(result)


class GetDetailsUrl:
    """
    根据列表页获取详情页的url
    """
    def __init__(self, list_url, co_index, page_list, encode=None, request_method=None, headers=None, analyzer='regex',
                 method='get', **kwargs):
        """

        :param list_url:
        :param co_index:
        :param page_list: 传递获取url的参数
        :param encode:
        :param request_method:
        :param headers:
        :param analyzer:
        :param method:
        :param kwargs:
        """
        self.list_url = list_url
        self.kwargs = kwargs
        self.encode = encode
        self.request_method = request_method
        self.headers = headers
        self.analyzer = analyzer
        self.method = method
        self.co_index = co_index
        self.page_list = page_list

    @retry(tries=3)
    def get_details(self):
        for i in self.list_url:
            try:
                html_ = do_request(i, self.method, self.headers, self.analyzer, self.encode)
                if self.page_list is not None:
                    # todo put in rabbitmq
                    """
                        rabbitmq data: json
                        {
                            "html": "html",
                            "co_index": "co_index",
                            "regex_list": [
                                {
                                "co_name": "regex"
                                }, 
                                {
                                "co_id": "id"
                                }
                            ]
                        }
                    
                    """
                    # 返回列表页url
                    return
                else:
                    # 没有需要选取的url，返回
                    print('没有需要选取的url，放入队列成功')
            except Exception as e:
                print(e)
                raise


if __name__ == '__main__':
    # h = {
    #     'Cache-Control': "no-cache",
    #     'User-Agent':
    #         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36'
    # }

    url = 'http://www.czfdc.gov.cn/spf/gs.php'
    b = AllListUrl(first_page_url=url,
                   request_method='get',
                   analyzer='xpath',
                   encode='gbk',
                   xpath='//*[@id="page_list"]/a[5]/span',
                   )
    b.get_page_count()
