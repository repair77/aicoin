# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from kafka import KafkaProducer
from mylog import MyLog

mylog = MyLog()


class Get30Pipeline():

    def __init__(self):

        self.produce = KafkaProducer(bootstrap_servers='47.91.220.218:9092', api_version=(0, 10, 1))

    def process_item(self, item):
        try:
            item_json = json.dumps(item, ensure_ascii=False).encode('utf-8')
            mylog.debug("write a piece data")
            self.produce.send('market-dev', item_json)
            self.produce.flush()
        except Exception as e:
            mylog.info("An error occurred while writing {}".format(e))