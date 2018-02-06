"""
url: http://61.178.148.157:8081/bit-xxzs/xmlpzs/nowwebissue.asp
city: 白银
num: 0
"""
import requests
from lxml import etree
import re
page = 0


class Baiyin:
    url = 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/nowwebissue.asp'
    page = page + 1
    def get_all_page(self):
        res = requests.get(url=self.url)
        html = res.content.decode('gb2312').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
        page = re.search(r'共有(.*?)页',html).group(1)
        print(page)
        return page

    def baiyin_start(self):
        page = self.get_all_page()
        for i in range(1, int(page) + 1):
            res = requests.get(self.url + '?page=' + page)
            html = res.content.decode('gb2312')
            tree = etree.HTML(html)
            community_list = tree.xpath('//tr[@align="center"]')
            for i in community_list:
                href = i.xpath('td/a/@href')
                if not href:
                    continue
                href = href[0]
                self.get_comm_detail(href)

    def get_comm_detail(self, href):
        comm_detail_url = 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/' + href
        print(comm_detail_url)
        response = requests.get(url=comm_detail_url)
        html = response.content.decode('gb2312').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
        co_name = re.search(r'项目名称(.*?)<td>(.*?)</td>',html).group(2)
        certificate = re.search(r'房屋所有权证号(.*?)<td>(.*?)</td>',html).group(2)
        approve_Times = re.search(r'批准时间(.*?)<td>(.*?)</td>',html).group(2)
        use = re.search(r'用　　途(.*?)<td>(.*?)</td>',html).group(2)
        project_type = re.search(r'项目类型(.*?)<td>(.*?)</td>',html).group(2)
        approve_area = re.search(r'批准面积(.*?)<td>(.*?)</td>',html).group(2)
        build_url = re.search(r'<td><ahref="(.*?)"',html)
        if build_url:
            build_url = build_url.group(1)
            self.get_build_detail(build_url)
        else:
            print('没有房屋信息')
        print(co_name, certificate, approve_Times, use, project_type, approve_area)
    def get_build_detail(self,build_url):
        build_detail_url = 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/' + build_url
        response = requests.get(url=build_detail_url)
        html = response.content.decode('gb2312').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
        build_name = re.search('项目名称(.*?)</td>(.*?)>(.*?)</td>',html).group(3)


if __name__ == '__main__':
    b = Baiyin()
    b.baiyin_start()