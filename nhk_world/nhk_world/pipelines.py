# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter
from nhk_world.items import NhkWorldItem

class NhkWorldPipeline:
    
    pipe_cnt = 0
    def open_spider(self, spider):
        
        self.enff = open('nhk_en_full.txt', 'w', encoding = 'utf-8')
        self.entf = open('nhk_en_title.txt', 'w', encoding = 'utf-8')
        self.enaf = open('nhk_en_article.txt', 'w', encoding = 'utf-8')
        
    def process_item(self, item, spider):
        self.pipe_cnt +=1
               
        item['article'] = ' '.join(item['article'])
        
        self.enff.write(f"{item['title']}|{item['article']}\n" )
        self.entf.write(f"{item['title']}\n")
        self.enaf.write(f"{item['article']}\n")
        
        print(f"{self.pipe_cnt:>3}: {item['title']}")
        
        return item

    
    def close_spider(self, spider):
        
        self.enff.close()
        self.entf.close()
        self.enaf.close()