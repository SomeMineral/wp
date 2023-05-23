# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from techdico.items import TechdicoItem
from itemadapter import ItemAdapter


class TechdicoPipeline:
    tech_cnt = 0
    
    def open_spider(self, spider):
        self.eng_f = open('eng_stc.txt', 'w', encoding = 'utf-8')
        self.kor_f = open('kor_stc.txt', 'w', encoding = 'utf-8')
        
    def process_item(self, item, spider):
        self.tech_cnt += 1
        
        self.eng_f.write(item['eng'] + '\n')
        self.kor_f.write(item['kor'] + '\n')
        
        print(f'Item counting : {self.tech_cnt:>5}')
        
        return item
    
    
    def close_spider(self, spider):
        self.eng_f.close()
        self.kor_f.close()