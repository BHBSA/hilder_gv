from crawler.guiyang_13 import Guiyang
from crawler.huzhou_19 import Huzhou
from crawler.xiamen_40 import Xiamen
from crawler.dongwan_9 import Dongwan
from crawler.jingmen_24 import Jingmen
from crawler.hangzhou_15 import Hangzhou

from crawler.kunming_26 import Kunming
from crawler.ninghai_35 import Ninghai
from crawler.foshan_10 import Foshan
from crawler.changshu_4 import Changshu
from crawler.yantai_58 import Yantai
from crawler.taian_50 import Taian
from crawler.xinyu_55 import Xinyu

from crawler.shenyang_45 import Shenyang
from crawler.taiyuan_49 import Taiyuan
from crawler.ningbo_33 import Ningbo
from crawler.yingtan_65 import Yingtai

if __name__ == '__main__':
    from multiprocessing import Process

    guiyang = Guiyang()
    Process(target=guiyang.start_crawler).start()
    huzhou = Huzhou()
    Process(target=huzhou.start_crawler).start()
    xiamen = Xiamen()
    Process(target=xiamen.start_crawler).start()
    kunming = Kunming()
    Process(target=kunming.start_crawler).start()
    dongwan = Dongwan()
    Process(target=dongwan.start_crawler).start()
    jingmen = Jingmen()
    Process(target=jingmen.start_crawler).start()
    hangzhou = Hangzhou()
    Process(target=hangzhou.start_crawler).start()

    shenyang_45 = Shenyang()
    Process(target=shenyang_45.start_crawler).start()

    taiyuan_49 = Taiyuan()
    Process(target=taiyuan_49.start_crawler).start()

    ningbo_33 = Ningbo()
    Process(target=ningbo_33.start_crawler).start()

    yingtan_65 = Yingtai()
    Process(target=yingtan_65.start_crawler).start()


    ninghai_35 = Ninghai()
    Process(target=ninghai_35.start_crawler).start()

    foshan_10 = Foshan()
    Process(target=foshan_10.start_crawler).start()

    changshu_4 = Changshu()
    Process(target=changshu_4.start_crawler).start()

    yantai_58 = Yantai()
    Process(target=yantai_58.start_crawler).start()

    taian_50 = Taian()
    Process(target=taian_50.start_crawler).start()

    xinyu_55 = Xinyu()
    Process(target=xinyu_55.start_crawler).start()