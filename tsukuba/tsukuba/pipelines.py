# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from tsukuba.items import TsukubaItem
# from tsukuba.items import TsukubaItem01, TsukubaItem02, TsukubaItem03, TsukubaItem04

import json
import os
import datetime

class TsukubaPipelineAll:
    all_cnt = 0
    
    def open_spider(self, spider):
        d = datetime.datetime.now()
        self.entire = open('entire_{}.txt'.format(d.strftime('%Y_%m_%d_%H%M')), 'a', encoding = 'utf-8')
        del d
        
    def close_spider(self, spider):
        self.entire.close()
        end_time = datetime.datetime.now()
        print('end_time : {}'.format(end_time.strftime('%Y_%m_%d_%H%M')))

    def process_item(self, item, spider):
        
        pro_cnt = 0
        for row in item['json_box']['rows']:
            self.entire.write(f"{row['example']}\n")
            self.all_cnt += 1
            pro_cnt += 1
        print('{0}_{1:0>3}/{2:0>3}'.format(item['hcid'],item['json_box']['page'],item['json_box']['total']))
        print('{0:0>8} completed({1:>7} added)'.format(self.all_cnt, pro_cnt))
        return item
