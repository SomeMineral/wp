# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from weblio_word.items import WeblioWordItem
from itemadapter import ItemAdapter
import re
import csv



class WeblioWordPipeline:
    
    pipe_cnt = 0
    
    def open_spider(self, spider):
        print('open_spider activates')
        self.fj = open('jp_word.txt', 'a', encoding = 'utf-8')
        self.fk = open('kr_word.txt', 'a', encoding = 'utf-8')
        self.fjk = open('jpkr_word.txt', 'a', encoding = 'utf-8')
        self.jk_writer= csv.writer(self.fjk)

        
    def process_item(self, item, spider):
        self.pipe_cnt += 1
        
        self.fj.write(f"{item['jp_word']}\n")
        
        for kr_word in item['kr_word']:
            self.fk.write(kr_word)
            self.fk.write(',')
        self.fk.write('\n')
        
        self.jk_writer.writerow([ item['jp_word'], item['kr_word'] ])
        
        print(f'write item in pipeline : {self.pipe_cnt:>6}')
        return item

    def close_spider(self, spider):
        print('close spider')
        fj.close()
        jk.close()
        fjk.close()