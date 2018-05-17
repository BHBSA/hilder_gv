from special_crawler.all_in_one import AllInOne
if __name__ == '__main__':
    sp_list_no_p = [
        # 庆阳
        {'url': 'http://60.165.104.70/bit-xxzs/xmlpzs/webissue.asp',
         'url_front': 'http://60.165.104.70/bit-xxzs/xmlpzs/', 'co_index': '155', },
    ]

    for i in sp_list_no_p:
        baiyin = AllInOne(url=i['url'], url_front=i['url_front'], co_index=i['co_index'], )
        baiyin.start_crawler()