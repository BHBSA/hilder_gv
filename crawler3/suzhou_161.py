"""
url = http://spf.szfcweb.com/szfcweb/(S(hdeijxnxs01rlpun22pnfha0))/DataSerach/SaleInfoProListIndex.aspx
city :  苏州
CO_INDEX : 161
author: 程纪文
"""
from crawler_base import Crawler
from comm_info import Comm, Building, House
import re, requests
import time
import json
import os
from lxml import etree
from lib.log import LogHandler

co_index = '161'
city_name = '苏州'
log = LogHandler('苏州')

class Suzhou(Crawler):
    def __init__(self):
        self.start_url = '3'
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36',
        }