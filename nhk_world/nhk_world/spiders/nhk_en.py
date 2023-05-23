import scrapy
import requests
from nhk_world.items import NhkWorldItem

class NhkEnSpider(scrapy.Spider):
    
    name = 'nhk_en' # 이건 손대지 말자.
    
    allowed_domains = ['www3.nhk.or.jp']
    main_url = 'https://www3.nhk.or.jp'
    
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.5,
        'BOT_NAME': 'jp_study',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'nhk_en_220908.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : True,
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'RETRY_TIMES': 10,
        'ITEM_PIPELINES' : {'nhk_world.pipelines.NhkWorldPipeline': 300},
    }
    
    global_keynames = ['en', 'ko', 'vi', 'ru', 'fr']
    # 다른 나라 기사도 찾아봤는데.. 영어 기사만 많이 있고 나머진....
    
    def start_requests(self):
        
        for global_keyname in self.global_keynames[:1]:
            json_url = f'{self.main_url}/nhkworld/data/{global_keyname}/news/archive.json'
            yield scrapy.Request(url = json_url, callback = self.json_parse)
        
    def json_parse(self, response):
        json_res = response.json()
        for data in json_res['data']:
            yield scrapy.Request(url = 'https://www3.nhk.or.jp' + data['page_url'], callback = self.news_collect)
    
    def news_collect(self, response):
        
        
        if response.status // 100 == 4:
            return None
        
        item = NhkWorldItem()
        item['title'] = response.xpath('//span[@class = "c-title__text"]/text()')[0].extract()
        item['article'] = [ chunk.replace('\n', ' ') for chunk in response.xpath('//div[@class = "p-article__body"]/p/text()').extract()]
        
        return item