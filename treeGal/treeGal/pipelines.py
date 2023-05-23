# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from treeGal.items import TreegalItem
from itemadapter import ItemAdapter

import os


class TreegalPipeline:
    
    pipe_cnt = 0
    
    def open_spider(self, spider):
        self.whole_number = open('whole_number.txt', 'a', encoding = 'utf-8')  
        self.whole_title = open('whole_title.txt', 'a', encoding = 'utf-8') 
        self.whole_main_text = open('whole_main_text.txt', 'a', encoding = 'utf-8')
    
    def process_item(self, item, spider):
        self.pipe_cnt += 1
        print(f'pipeline start : {self.pipe_cnt}')

        self.whole_number.write(item['number'])
        self.whole_number.write('\n')
        self.whole_title.write(item['title'])
        self.whole_title.write('\n')
        self.whole_main_text.write(item['main_text'])
        self.whole_main_text.write('\n')

        print(f'pipeline end : {self.pipe_cnt}')
        print(f"<<<<number>>>> : {item['number']}")
        return item
    
    def close_spider(self, spider):
        self.whole_number.close()
        self.whole_title.close()
        self.whole_main_text.close()
        