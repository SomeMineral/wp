# scrapy crawl EngRus_w -s JOBDIR=crawls/EngRus_w-1
# only word extract

import scrapy
from scrapy import Spider, signals

from trex_en.items import EngRusWItem
import time


class EngRusSpider(scrapy.Spider):
    
    name = 'EngRus_w'
    allowed_domains = ['tr-ex.me']
    basic_url = 'https://tr-ex.me'
    language = 'english-russian'

    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 1.0,
        'BOT_NAME': 'eng_rus_study',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'eng_rus_w.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : True,
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'ITEM_PIPELINES' : {'trex_en.pipelines.TrexEnWordPipeline': 100},
        #'SPIDER_MIDDLEWARES' : {'trex_en.middlewares.TimeOutDownloaderMiddleware': 543},
        'RETRY_TIMES': 10,
    }
    
    cnt = 0
    
    def start_requests(self):
        basic_queries = f'{self.basic_url}/queries/{self.language}/words/'
        
        start_time = time.time()
        
        #start = 1
        #end = 240852
        temp_start = 20000
        temp_end = 240852
        
        increment = 1000
        
        for start in range(temp_start, temp_end, increment):  
            range_queries = basic_queries + f'{start}-{start + increment}.html'
            yield scrapy.Request(url = range_queries, callback = self.word_selector)
    
    def word_selector(self, response):
        words = response.xpath('//div[@class = "item"]/a[@class = "query"]/text()').extract()
        frame_url = f'{self.basic_url}/translation/{self.language}/'
        
        for word in words:
            yield scrapy.Request(url = frame_url + word, callback = self.word_miner)
    
    
    def word_miner(self, response):
        item = EngRusWItem()       
        item['w_Eng'] = response.xpath('//div[@id = "contexts"]//span[@class = "query-highlight"]/text()')[0].extract()

        word_translation_tag = response.xpath('//div[@id = "query"]')
        if word_translation_tag == []:
            item['w_Rus'] = ' '
        else:
            item['w_Rus'] = word_translation_tag.xpath('.//span[@class = "text"]/text()').extract()
               
        self.cnt += 1
        print(f"{self.cnt} - {item['w_Eng']}\n{item['w_Rus']}")  
                
        yield item