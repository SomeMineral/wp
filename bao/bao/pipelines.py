# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class BaoPipeline:
    
    pipe_cnt = 0
    
    def open_spider(self, spider):
        
        self.f_url = open('bao_url.txt', 'a', encoding = 'utf-8')
        self.f_title = open('bao_title.txt', 'a', encoding = 'utf-8')
        
        self.f_eng_article = open('bao_eng_article.txt', 'a', encoding = 'utf-8')
        self.f_viet_article = open('bao_viet_article.txt', 'a', encoding = 'utf-8')
        
        self.f_eng_paragraph = open('bao_eng_paragraph.txt', 'a', encoding = 'utf-8')
        self.f_viet_paragraph = open('bao_viet_paragraph.txt', 'a', encoding = 'utf-8')
        
    
    def process_item(self, item, spider):
        
        # eng first, viet next in item['article']
        
        eng_box = []
        viet_box = []
        
        #cmp = re.compile('[\W\s\d“”‘’]+')
        cmp = re.compile(r'[\W\s\d\u2000-\u2040\u0021-\u002F]+')
    
        cmp2 = re.compile('[a-zA-Z]+')
        
        for idx, piece in enumerate(item['article']):
            
            temp = cmp.sub("", piece)
            temp2 = cmp2.search(temp)
            
            if ( temp2.end() - temp2.start() ) == len(temp):
                eng_box.append(piece)
                
            else:
                viet_box.append(piece)     
        
        
        if len(eng_box) == len(viet_box):
            for piece_e in eng_box:
                self.f_eng_paragraph.write(piece_e)
                self.f_eng_paragraph.write('\n')                
            for piece_v in viet_box:
                self.f_viet_paragraph.write(piece_v)
                self.f_viet_paragraph.write('\n')
            
            self.f_url.write(item['url'])
            self.f_url.write('\n')

            self.f_title.write(item['title'])
            self.f_title.write('\n')

            item['eng'] = ' '.join(eng_box)
            item['viet'] = ' '.join(viet_box)     

            self.f_eng_article.write(item['eng'])
            self.f_eng_article.write('\n')

            self.f_viet_article.write(item['viet'])
            self.f_viet_article.write('\n')

            self.pipe_cnt += 1
            print(f'saved : {self.pipe_cnt:5>}')
            
        else:
            print(f"eng, viet 개수가 다른데요? {item['url']}")


        return item


    def close_spider(self, spider):
        
        self.f_url.close()
        self.f_title.close()
        
        self.f_eng_article.close() 
        self.f_viet_article.close()
        
        self.f_eng_paragraph.close()
        self.f_viet_paragraph.close()