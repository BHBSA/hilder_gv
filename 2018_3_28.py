from crawler.chengdu_5 import Chengdu
from crawler.cixi_8 import Cixi
from crawler.jieyang_23 import Jieyang
from crawler.jingmen_24 import Jingmen
from crawler.loudi_29 import Loudi
from crawler.xiamen_40 import Xiamen
from crawler.yichun_64 import Yichun
from crawler.zaozhuang_68 import Zaozhuang
from crawler.wenzhou_53 import Wenzhou

from multiprocessing import Process

if __name__ == '__main__':
    chengdu = Chengdu()
    cixi = Cixi()
    jieyang = Jieyang()
    jingmen = Jingmen()
    loudi = Loudi()
    xiamen = Xiamen()
    yichun = Yichun()
    zaozhuang = Zaozhuang()
    wenzhou = Wenzhou()
    Process(target=chengdu.start_crawler).start()
    Process(target=cixi.start_crawler).start()
    Process(target=jieyang.start_crawler).start()
    Process(target=jingmen.start_crawler).start()
    Process(target=loudi.start_crawler).start()
    Process(target=xiamen.start_crawler).start()
    Process(target=yichun.start_crawler).start()
    Process(target=zaozhuang.start_crawler).start()
    Process(target=wenzhou.start_crawler).start()

    from special_crawler.all_in_one import AllInOne
    from special_crawler.not_in_one import NotAllInOne

    sp_list_no_p = [
        # 本溪
        {'url': 'http://gs.bxfdc.cn/xmlpzs/webissue.asp?',
         'url_front': 'http://gs.bxfdc.cn/xmlpzs/', 'co_index': '1025', },
        # 呼和浩特
        {'url': 'http://60.31.254.197/bit-xxzs/xmlpzs/webissue.asp',
         'url_front': 'http://60.31.254.197/bit-xxzs/xmlpzs/', 'co_index': '1027', },
        # 景德镇
        {'url': 'http://www.jdzfgj.cn/bit-xxzs/xmlpzs/nowwebissue.asp',
         'url_front': 'http://www.jdzfgj.cn/bit-xxzs/xmlpzs/', 'co_index': '1028', },
        # 临沂
        {'url': 'http://lyfdc.gov.cn:88/bit-xxzs/xmlpzs/webissue.asp?',
         'url_front': 'http://lyfdc.gov.cn:88/bit-xxzs/xmlpzs/', 'co_index': '1030', },
        # 渭南
        {'url': 'http://www.wnfdc.com/bit-xxzs/xmlpzs/webissue.asp',
         'url_front': 'http://www.wnfdc.com/bit-xxzs/xmlpzs/', 'co_index': '1031', },
        # 西宁
        {'url': 'http://www.xnfcxx.com/bit-xxzs/xmlpzs/webissue.asp',
         'url_front': 'http://www.xnfcxx.com/bit-xxzs/xmlpzs/', 'co_index': '1032', },
        # 许昌
        {'url': 'http://222.89.166.137/bit-xxzs/xmlpzs/webissue.asp',
         'url_front': 'http://222.89.166.137/bit-xxzs/xmlpzs/', 'co_index': '1033', },
        # 白银
        {'url': 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/nowwebissue.asp',
         'url_front': 'http://61.178.148.157:8081/bit-xxzs/xmlpzs/', 'co_index': '0', },
        # 宝鸡
        {'url': 'http://61.185.69.154/bit-xxzs/xmlpzs/webissue.asp?',
         'url_front': 'http://61.185.69.154/bit-xxzs/xmlpzs/', 'co_index': '1024'},
        # 东营
        {'url': 'http://www.dyfc.gov.cn/bit-xxzs/xmlpzs/nowwebissue.asp?',
         'url_front': 'http://www.dyfc.gov.cn/bit-xxzs/xmlpzs/', 'co_index': '1026', },
    ]
    for i in sp_list_no_p:
        baiyin = AllInOne(url=i['url'], url_front=i['url_front'], co_index=i['co_index'], )
        Process(target=baiyin.start_crawler).start()

    not_sp_list_no_p = [
        # 莱芜
        {'url': 'http://www.lwfccs.com/bit-xxzs/xmlpzs/prewebissue.asp?',
         'url_front': 'http://www.lwfccs.com/bit-xxzs/xmlpzs/', 'co_index': '1029', },
    ]
    for i in not_sp_list_no_p:
        not_all_one = NotAllInOne(url=i['url'], url_front=i['url_front'], co_index=i['co_index'], )
        not_all_one.start_crawler()
