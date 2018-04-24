import requests
import random
from lib.log import LogHandler

log = LogHandler('proxy')

class Proxy_contact():
    def __init__(self,app_name=None,method=None,url=None,ban_word=None,formdata=None):
        self.user_agent_list = [
            {"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko"},
            {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},

        ]           #pc端浏览器
        self.app_name = app_name
        self.method = method
        self.url = url
        self.ban_word = ban_word
        self.formdata = formdata

    def headers(self):
        index = random.randint(0,4)
        user_agent = self.user_agent_list[index]
        headers = {
            "User-Agent":user_agent["User-Agent"],
        }
        return headers

    def contact(self):
        try:
            if self.method == 'get':
                count = 0
                while True:
                    proxy_ip = self.get_proxy()
                    proxies = {"http": "http://" + proxy_ip}
                    try:
                        res = requests.get(self.url,proxies=proxies,headers=self.headers(),timeout=10,)
                        if res.status_code == 200:
                            # if self.ban_word in res.content.decode(self.encode):
                            #     self.post_back(proxy_ip, 1)
                            self.post_back(proxy_ip, 0)
                            break
                        else:
                            continue
                    except:
                        self.post_back(proxy_ip, 1)
                        count += 1
                        log.debug("尝试第{}次重新连接".format(count))
                        continue
                return res.content
            elif self.method == 'post':
                count = 0
                while True:
                    proxy_ip = self.get_proxy()
                    proxies = {"http": ("http://" + proxy_ip)}
                    try:
                        res = requests.post(self.url,data=self.formdata,proxies=proxies,headers=self.headers(),timeout=10)
                        if res.status_code ==200:
                            self.post_back(proxy_ip, 0)
                            break
                        else:
                            continue
                    except:
                        self.post_back(proxy_ip,1)
                        count += 1
                        log.info("尝试第{}次重新连接".format(count))
                        continue
                return res.content
            else:
                log.error("method wrong！")
        except Exception as e:
            log.error(e)


    def get_proxy(self):
        api_1 = "http://127.0.0.1:8999/get_one_proxy"
        app_name = self.app_name
        data = {"app_name":app_name,}

        proxy_ip = requests.post(api_1, data=data).text

        return proxy_ip

    def post_back(self,ip,code):
        api_2="http://127.0.0.1:8999/send_proxy_status"
        data = {
            "app_name":self.app_name,
            "ip":ip,
            "status_code":code,
        }
        requests.post(api_2, data=data)

