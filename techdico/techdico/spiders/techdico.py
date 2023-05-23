import scrapy
import time
import random

from techdico.items import TechdicoItem


class TechdicoSpider(scrapy.Spider):
    name = 'techdico'
    allowed_domains = ['www.techdico.com']
    
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.5,
        'BOT_NAME': 'tech_study',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'techdico.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : False, # 으악! 여긴 다 막아뒀네
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'RETRY_TIMES': 10,
        'ITEM_PIPELINES' : {'techdico.pipelines.TechdicoPipeline': 300},
    }
    
    
    def start_requests(self):
        with open('c:/users/user/desktop/general/box3.txt', 'r', encoding = 'utf-8') as word_f:
            word_cnt = 0
            for word in word_f:
                time.sleep(random.uniform(1, 2))
                               
                # --test--up----
                #if word_cnt > 10:
                #    return None
                # --test--down--
                
                temp = word.strip()
                basic_url = 'https://www.techdico.com/translation/english-korean/'
                url = basic_url + temp + '.html'
                
                print(f'[{word_cnt:0>4}] {url}')
                word_cnt += 1
                
                yield scrapy.Request(url = url, callback = self.tech_finding)
                
    def tech_finding(self, response):
        print('hoho')
        time.sleep(random.uniform(1, 2))
        some_tags = response.xpath('//div[@class = "resblk"]')
        
        if len(some_tags) == 2:
            dict_stc_tags = some_tags[0].xpath('.//div[@class = "tradGroup"]')
            for dict_stc_tag in dict_stc_tags:
                item = TechdicoItem()
                item['eng'] = ''.join(dict_stc_tag.xpath('.//div[@class="col-xs-6"]/h2/text()').extract()) 
                itme['kor'] = dict_stc_tag.xpath('.//div[@class="col-xs-6 colleft"]//a/text()')[0].extract()
                
                yield item
        
        cont_stc_tags = some_tags[-1].xpath('.//div[@class="sentn clearfix decalexparrow"]')
        for cont_stc_tag in cont_stc_tags:
            item = TechdicoItem()
            item['eng'] = ''.join(cont_stc_tag.xpath('.//div[@class="col-xs-6"]//*[self::span or self::a or self::b]/text()').extract())
            item['kor'] = cont_stc_tag.xpath('.//div[@class="col-xs-6 colleft"]//span/text()')[0].extract()
            yield item
        
        
            
