import scrapy
import requests

from jjalbang.items import JjalbangItem


class ImgCollectSpider(scrapy.Spider):
    name = 'img_collect'
    allowed_domains = ['jjalbang.today']
    start_urls = ['https://jjalbang.today']
    
    custom_settings = {
    'RANDOMIZE_DOWNLOAD_DELAY': True,
    'DOWNLOAD_DELAY': 1.5,
    'BOT_NAME': 'jbcollectbot',
    'LOG_LEVEL': 'ERROR',
    'LOG_FILE':'jjalbang.log',  # log 파일 위치
    'CONCURRENT_REQUESTS' : 10,
    'HTTPCACHE_ENABLED' : True
    }   

    
    
    def __init__(self):
        self.basic_url ='https://jjalbang.today'
        self.tag = '분노'

    def parse(self, response):
        
        for p in range(1,100):
            page_url = f'{self.basic_url}/ajax/jjalbang_list.php?tag={self.tag}&page={p}&mode='
            print(f'{page_url=}')
            page = requests.get(url = page_url)
            page_js = page.json()
            
            if page_js[0]['page_end'] == 'end':
                print('********** No result *********')
                return None
                
            for content in page_js:
                sub_url = content['lc_imgurl']
                
                if sub_url.startswith('http'):
                    continue #외부 그림은 생략
                
                sub_urls = sub_url.replace('_data','files')
                
                yield scrapy.Request( url = self.basic_url + sub_urls, callback = self.parse_urls)
    
    
    def parse_urls(self, response):
        
        item = JjalbangItem()
        
        ## 파일의 url을 사용할 때는 list 형태로 넣어줘야 하는건..가?
        item['image_urls'] = [response.url]
        
        return item
        