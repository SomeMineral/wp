# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
from japan_novel.items import JapanShortNovelItem, JapanLongNovelItem

class JapanNovelPipeline:
    
    #def open_spider(self, spider):
    #def close_spider(self, spider):

    
    def process_item(self, item, spider):
        if isinstance(item, JapanShortNovelItem):
            return self.short_pipe(item, spider)
        
        if isinstance(item, JapanLongNovelItem):
            return self.long_pipe(item, spider)
    
    def short_pipe(self, item, spider):
        #print("Here is short_pipe.")
        if os.path.isfile(f"novel_box/{item['novel_code']}.txt"):
            return None
        
        else:
            with open(f"novel_box/{item['novel_code']}.txt", 'w', encoding = 'utf-8') as sp:
                sp.write("[title]\n")
                sp.write(f"{item['title']}\n")
                sp.write("==========\n")
                num_of_lines = len(item['text'])
                
                for idx, line in enumerate(item['text'], start = 1):
                    sp.write(line)
                    if idx == num_of_lines:
                        break
                    sp.write('\n')
            print(f"pipe - {item['novel_code']}")
            return item
        
        
    def long_pipe(self, item, spider):
        #print("Here is long_pipe.")
        if os.path.isfile(f"novel_box/{item['novel_code']}/{item['list_num']:0>4}.txt"):
            return None
        
        else:
            with open(f"novel_box/{item['novel_code']}/{item['list_num']:0>4}.txt", 'w', encoding = 'utf-8') as lp:
                lp.write("[subtitle]\n")
                lp.write(f"{item['subtitle']}\n")
                lp.write("==========\n")
                
                num_of_lines = len(item['text'])
                
                for idx, line in enumerate(item['text'], start = 1):
                    lp.write(line)
                    if idx == num_of_lines:
                        break
                    lp.write('\n')
            print(f"pipe - {item['novel_code']}_{item['list_num']:0>4}")
            return item
                