# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import re
import csv
from trex_en.items import EngRusWItem, EngRusSItem


class TrexEnPipeline:    
    
    def open_spider(self, spider):
        self.wf = open('word_EngRus.csv', 'a', encoding = 'utf-8')
        self.word_writer = csv.writer(self.wf)
        self.word_writer.writerow( ['Eng', 'Rus'] )
        
        self.sf = open('sentence_EngRus.csv', 'a', encoding = 'utf-8')
        self.sentence_writer = csv.writer(self.sf)
        self.sentence_writer.writerow( ['Eng-Rus_word_pairs'] )
    
        self.esef = open('each_sentence_Eng.csv', 'a', encoding = 'utf-8')
        self.each_se_writer = csv.writer(self.esef)
        self.each_se_writer.writerow( ['Eng'] )
        
        self.esrf = open('each_sentence_Rus.csv', 'a', encoding = 'utf-8')
        self.each_sr_writer = csv.writer(self.esrf)
        self.each_sr_writer.writerow( ['Rus'] )
        
    def process_item(self, item, spider):
        
        if isinstance(item, EngRusWItem):
            return self.Wpipe(item, spider)
        
        if isinstance(item, EngRusSItem):
            return self.Spipe(item, spider)
    
    
    def Wpipe(self, item, spider):
        self.word_writer.writerow( (item['w_Eng'], item['w_Rus']) )
        
        return item
       
        
    def Spipe(self, item, spider):
        self.sentence_writer.writerow(item['s_EngRus'])
        self.each_se_writer.writerow([item['s_EngRus'][0]])
        self.each_sr_writer.writerow([item['s_EngRus'][1]])
        
        return item
    
    
    def close_spider(self, spider):
        
        self.wf.close()
        self.sf.close()
        self.esef.close()
        self.esrf.close()
        


class TrexEnWordPipeline:    
    
    def open_spider(self, spider):
        self.wf = open('word_EngRus.csv', 'a', encoding = 'utf-8')
        self.word_writer = csv.writer(self.wf)
        self.word_writer.writerow( ['Eng', 'Rus'] )

    def process_item(self, item, spider):
        self.word_writer.writerow( (item['w_Eng'], item['w_Rus']) )
        
        return item  
    
    def close_spider(self, spider):
        self.wf.close()
