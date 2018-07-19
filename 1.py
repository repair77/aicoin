# coding:utf-8

import requests
import json
import time


def Ttex():
    head_url = "https://www.ttex.com"
    url = "https://www.huobi.pro/-/x/general/index/constituent_symbol/detail?r=p1ko92b4mml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    try:
        response = requests.get(url, headers=headers).text
    except:
        return None
    Data_list = json.loads(response)
    content = []
    for Data in Data_list['data']['symbols']:
        item = {}
        item['symbol'] = Data['name'].upper()
        item['unit'] = Data['symbol'].replace(Data['name'], "")
        item['from'] = "web1"
        item['exchange'] = "Huobi"
        item['last'] = Data['close']
        item['volume'] = 0
        item['high'] = Data['open']
        item['low'] = 0
        item['measurement'] = "market"
        item['timestamp'] = int(time.time())
        item['onlyKey'] = "{}_{}_{}".format(item['exchange'], item['symbol'], item['unit'])
        item['change'] = Data['rise_percent']
        item['timeFrom'] = "symtem"
        content.append(item)
    return json.dumps(content)

print Ttex()

