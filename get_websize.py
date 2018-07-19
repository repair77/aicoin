# coding:utf-8
import time
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from mylog import MyLog
from pipelines import Get30Pipeline


class get_requests():
    head_url = "https://www.aicoin.net.cn/chart/5C79AC2D"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    timeout = 0
    kfk = Get30Pipeline()

    def get_head(self):
        log.debug("正在请求列表信息")
        response = requests.get(self.head_url, headers=self.headers).text
        cat = re.findall('window\.COINS = (.*?);', response, re.S)[0]
        data = json.loads(cat)
        for i in data:
            keys = i['key']
            if i['mid'] == "okcoinfutures":
                mid = "okex"
            else:
                mid = i['mid']
            bName = i['coin']
            unit = i['currency']
            symbol = i['symbol']
            self.get_data(symbol, keys, unit, bName, mid)
            

    def get_data(self, symbol, key, unit, bName, mid):
        url = "https://www.aicoin.net.cn/chart/api/data/period?symbol={}&step=86400".format(symbol)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Referer": "https://www.aicoin.net.cn/chart/{}".format(key)
        }
        log.debug("正在爬取{}的{}".format(symbol, unit))
        if self.timeout > 10:
            log.debug("网站请求出现异常，请打开页面是否已经被反爬{}".format(self.head_url))
        time.sleep(2)
        try:
            response = json.loads(requests.get(url, headers=headers, timeout=5).text)
        except:
            log.debug("网站请求出现异常，请打开页面是否已经被反爬{}".format(self.head_url))
            self.timeout += 1
            return ''


        content = []
        count = response['count']
        try:

            for data in response['data']:
                item = {}
                item['onlyKey'] = mid[0].upper() + mid[1:] + "_" + bName.upper() + "_" + unit.upper()
                item['type'] = "Alcoin"
                item['Measurement'] = "kline"
                item['Timestamp'] = int(data[0]) * 1000
                item['Open'] = data[1]
                item['High'] = data[2]
                item['Low'] = data[3]
                item['Close'] = data[4]
                item['Volume'] = data[5]
                content.append(item)

            for i in range(1, 3):
                url_ = "https://www.aicoin.net.cn/chart/api/data/periodHistory?symbol=okcoinfuturesbtcweekusd&step=86400&times={}".format(
                    i)
                data = {
                    "symbol": symbol,
                    "step": "86400",
                    "tunes": i,
                    "count": count,
                }

                response = json.loads(requests.post(url_, headers=headers, data=data).text)
                if response:
                    for data in response:
                        item = {}
                        item['onlyKey'] = mid[0].upper() + mid[1:] + "_" + bName.upper() + "_" + unit.upper()
                        item['type'] = "Alcoin"
                        item['Measurement'] = "kline"
                        item['Timestamp'] = int(data[0]) * 1000
                        item['Open'] = data[1]
                        item['High'] = data[2]
                        item['Low'] = data[3]
                        item['Close'] = data[4]
                        item['Volume'] = data[5]
                        content.append(item)
            self.kfk.process_item(content)
        except Exception as e:
            log.info("this data an error {}".format(e))


if __name__ == '__main__':
    log = MyLog()
    log.debug("程序正在运行·····")
    a = get_requests()
    a.get_head()