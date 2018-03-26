from crawler_base import Crawler


class Qingyuan(Crawler):
    def __init__(self):
        self.url = 'http://www.qyfgj.cn/newys/user_kfs.aspx'
        self.co_index = 38

    def start_crawler(self):
        page_count = self.get_all_page()

    def get_all_page(self):
        pass
