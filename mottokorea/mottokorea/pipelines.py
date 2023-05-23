# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from mottokorea.items import MottokoreaErrorItem, MottokoreaItem



class MottokoreaPipeline:
    
    working_cnt = 0
    error_cnt = 0
    
    def open_spider(self, spider):
        self.kr_expr = open('korean_expression.txt', 'w', encoding = 'utf-8') 
        self.jp_mean = open('japanese_meaning.txt', 'w', encoding = 'utf-8')
        self.error_url = open('error_url.txt', 'w', encoding = 'utf-8')
    
    def process_item(self, item, spider):        
        if isinstance(item, MottokoreaItem):
            return self.working(item, spider)
        
        if isinstance(item, MottokoreaErrorItem):
            return self.error_collector(item, spider)
    
    def working(self, item, spider):
        self.kr_expr.write(f"{item['kr_expr']}\n")
        self.jp_mean.write(f"{item['jp_mean']}\n")
        self.working_cnt += 1
        
        print(f"{self.working_cnt:>4} | {item['kr_expr']} | {item['jp_mean']}")
        return item
    
    def error_collector(self, item, spider):
        self.error_url.write(f"{item['error_url']}\n")
        self.error_cnt += 1
        print(f"error count : {self.error_cnt:>4}")
        return item
    
    def close_spider(self, spider):
        self.kr_expr.close()
        self.jp_mean.close()
        self.error_url.close()