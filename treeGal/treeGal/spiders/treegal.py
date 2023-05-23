import os
import random
import re
import scrapy
import time
from treeGal.items import TreegalItem

class TreegalSpider(scrapy.Spider):
    name = 'treegal'
    allowed_domains = ['gall.dcinside.com']

    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.8,
        'BOT_NAME': 'please',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'treegal.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : False, # 으으.. 디씨... 싸우자? 
        'DEFAULT_REQUEST_HEADERS' : {'Referer' : 'https://search.dcinside.com/'},
        'FEED_EXPORT_ENCODING' : 'utf-8',
        
        'RETRY_ENABLED' : True,
        'RETRY_TIMES': 2,
        
        'ITEM_PIPELINES' : {'treeGal.pipelines.TreegalPipeline': 300},
        'DOWNLOADER_MIDDLEWARES' : {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                                    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
                                    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
                                    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
                                   }
    }
    
    def start_requests(self):
        
        start_number = 3419623
        end_number = 335100 # 335100 2013년 1월 1일 첫 글.
        tree_url_form = 'https://gall.dcinside.com/board/view/?id=theaterM&no='  # 연극, 뮤지컬 갤러리
        
        req_cnt = 0
        
        for number in range(start_number, end_number-1, -1):
            
            if os.path.exists(f"treeBox/{number}.txt"):
                print(f"It already exists.: {number}")
                continue
                
            req_cnt += 1
            
            if req_cnt % 50 == 0:
                print("It's time to take some rest.")
                time.sleep(random.uniform(15,20))
                
            time.sleep(random.uniform(1,3))
            yield scrapy.Request(url = f'{tree_url_form}{number}', callback = self.text_collector)
            
            
    def text_collector(self, response):
        
        if response.status == 404:
            print(f'{response.status} : {response.url}')
            return None
         
        print('pass')
        
        item = TreegalItem()  
        item['number'] = re.search('no=[0-9]*',response.url)[0].replace('no=','')
        print('number pass')
                
        item['title'] = response.xpath('//span[@class="title_subject"]/text()')[0].extract()
        print('title pass')
        
        main_text = response.xpath('//div[@class="write_div"]').xpath('descendant-or-self::p/text() | descendant-or-self::div/text() | descendant-or-self::span/text()').extract()
        main_text = [word.strip() for word in main_text]
        main_text = [word.replace('\n','') for word in main_text] # 221122 추가
        main_text = [word for word in main_text if (word != '') and (word is not None) and (word != '\n')] # 221124 추가 // 221219 추가 흑흑
        
        item['main_text'] = ' '.join(main_text)
        print('main_text pass')
        
        return item