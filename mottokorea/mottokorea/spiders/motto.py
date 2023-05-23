import re
import scrapy
from mottokorea.items import MottokoreaErrorItem, MottokoreaItem 


class MottoSpider(scrapy.Spider):
    name = 'motto'
    allowed_domains = ['mottokorea.com']
    
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.5,
        'BOT_NAME': 'shiritai',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'motto.log',  # log 파일 위치
        'FEED_EXPORT_ENCODING' : 'utf-8',
        
        'RETRY_ENABLED' : True,
        'RETRY_TIMES': 2,
        
        'ITEM_PIPELINES' : {'mottokorea.pipelines.MottokoreaPipeline': 300},
    }
    
    def start_requests(self):
        list_basic = 'https://mottokorea.com/mottoKoreaW/Vocabulary_list.do?pageNum='
        # 88까지는 의미와 해설이 나뉘어 있는데
        # 89부터는 섞여있음.. 흠
        # 물론 1~88 사이에도 형식에 안 맞는 게 있을 가능성이 있지.
        
        for num in range(1,88+1):
            yield scrapy.Request(url = list_basic + str(num), callback = self.url_extractor)
        
    def url_extractor(self, response):
        
        content_basic = 'https://mottokorea.com/mottoKoreaW/'
        partial_urls = response.xpath('//tbody[@id="ask"]/tr/td/a/@href').extract()
        
        for partial_url in partial_urls:
            yield scrapy.Request(url = content_basic + partial_url, callback = self.content_extractor)
    
    def content_extractor(self, response):
        
        content_bag = response.xpath('//td[@class="Atext_after_korea"]/text()').extract()
        
        try:
            temp_kr = content_bag[0].split('：')[1].strip()
            item = MottokoreaItem()
            item['kr_expr'] = temp_kr
            
            temp_jp = content_bag[2].split('：')[1].strip()
            if temp_jp == '':
                raise Exception
            item['jp_mean'] = temp_jp
        
        # '：'와 ':'는 달랐다... 폰트 무서워
        
        except:
            item = MottokoreaErrorItem()
            item['error_url'] = response.url
        
        if isinstance(item, MottokoreaItem):
            print('정상')
        if isinstance(item, MottokoreaErrorItem):
            print('문제 있음')
        
        return item