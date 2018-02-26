import requests
from lxml import etree
import re


class AllListUrl:
    """
    获取所有列表页的url
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

    def decode(self, result):
        if self.encode:
            html_content = result.content.decode(self.encode)
        else:
            html_content = result.content.decode()
        return html_content

    def do_request(self, url, method):
        """

        :param url:
        :param method:'get', 'post'
        :return: html_tree
        """
        if method is 'get':
            result = requests.get(url, headers=self.headers)
            if self.analyzer is 'xpath':
                html_tree = self.decode(result, )
                return etree.HTML(html_tree)
            else:
                html_tree = self.decode(result, )
                return html_tree
        else:
            # todo post
            pass

    def get_page_count(self, ):
        html_ = self.do_request(self.first_page_url, self.method)
        if self.analyzer is 'xpath':
            print('开始xpath')
            page_xpath = self.kwargs.get('xpath')
            print(page_xpath)
            result = html_.xpath(page_xpath)[0]
            print(int(result.text))
            return int(result.text)
        else:
            print('开始正则')
            # print(html_)
            page_regex = self.kwargs.get('regex')
            group_regex = self.kwargs.get('regex_group')
            result = re.search(page_regex, html_, re.M | re.S).group(group_regex)
            print(int(result))
            return int(result)


if __name__ == '__main__':
    # b = AllListUrl(first_page_url='http://www.gyfc.net.cn/2_proInfo/index.aspx', method='get',
    #                xpath='//*[@id="ProInfo1_AspNetPager1"]/div[1]/font[2]/b')
    h = {
        'Cache-Control': "no-cache",
        # 'Postman-Token': "26a4f1b5-dfa9-1e9f-8b80-61e1e9c50f58",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    b = AllListUrl(first_page_url='http://www.gyfc.net.cn/2_proInfo/index.aspx',
                   split_url='http://www.gyfc.net.cn/2_proInfo/index.aspx?page=', request_method='get',
                   analyzer='xpath', regex_group=2, encode='gbk', headers=h,
                   xpath='//*[@id="ProInfo1_AspNetPager1"]/div[1]/font[2]/b')
    b.get_page_count()
