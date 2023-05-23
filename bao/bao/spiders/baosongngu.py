# scrapy crawl baosongngu -s JOBDIR=crawls/baosongngu-1

import scrapy

from bao.items import BaoItem


class BaosongnguSpider(scrapy.Spider):

    name = 'baosongngu'
    allowed_domains = ['baosongngu.net']
    start_urls = ['https://baosongngu.net/chuyen-muc']
    article_cnt = 0

    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 1.0,
        'BOT_NAME': 'study_hard',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'bao.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : True,
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'CONCURRENT_REQUESTS' : 10,
        'ITEM_PIPELINES' : { 'bao.pipelines.BaoPipeline': 300 }
    }       
    
    def start_requests(self):
        main_url = 'https://baosongngu.net/chuyen-muc/vn/page/'
        for num in range(1, 53 + 1):
            yield scrapy.Request(url = f'{main_url}{str(num)}', callback = self.find_urls)
    
    def find_urls(self, response):
        url_list = response.xpath('//article[contains(@id, "post")]//h2/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url = url, callback = self.extract_articles)
    
    def extract_articles(self, response):      
        title = response.xpath('//h1/text()')[0].extract()   
        
        article_box = []
        article_tag = response.xpath('//div[@class = "inner-post-entry entry-content"]//p')
        
        
        
        for tag in article_tag:
            
            if tag.xpath('.//img'):
                continue
            if tag.xpath('attribute::id'):
                continue
            
            pieces = [piece.strip() for piece in tag.xpath('./text() | .//*[self::span or self::strong or self::em or self::b or self::i]/text()').extract()]        
            
            paragraph = ' '.join(pieces)
            
            article_tag[15].xpath('.//*[contains(@id,"caption")]')
            
            if 'Nguồn' in paragraph or 'Từ mới:' in paragraph or 'html' in paragraph:
                break
            if paragraph in ['',' ','\n']:
                continue
           
            article_box.append(paragraph)
        
        item = BaoItem()
        item['url'] = response.url
        item['title'] = title
        item['article'] = article_box
        
        self.article_cnt += 1
        
        print(f'article extracted : {self.article_cnt:>5}')
        
        return item