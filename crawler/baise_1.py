"""
url = http://www.bsfcj.com/PubInfo/HouseSource.asp?page=1&xm_xzqy=&xm_xmmc=&xm_xmdz=&xm_kfs=&xm_fwhx=
city: 百色
CO_INDEX: 1
"""
CO_INDEX = 1
import requests
from lxml import etree


class Baise:
    url = 'http://www.bsfcj.com/PubInfo/HouseSource.asp?page=1&xm_xzqy=&xm_xmmc=&xm_xmdz=&xm_kfs=&xm_fwhx='

    def baise_start(self):
        requests.get(url=self.url)

    def get_all_page(self):
        res = requests.get(url=self.url)
        html = etree.HTML(res.content.decode('gb2312'))
        html.xpath('')


if __name__ == '__main__':
    b = Baise()
    b.get_all_page()
