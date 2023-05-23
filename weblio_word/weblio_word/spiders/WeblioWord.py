#scrapy crawl WeblioWord -s JOBDIR=crawls/WeblioWord-1

import scrapy
from weblio_word.items import WeblioWordItem

class WeblioWordSpider(scrapy.Spider):
    name = 'WeblioWord'
    allowed_domains = ['kjjk.weblio.jp']
    start_urls = ['https://kjjk.weblio.jp/']
    
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 1.0,
        'BOT_NAME': 'study_hard',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'weblio_word.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : True,
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'CONCURRENT_REQUESTS' : 10,
        'ITEM_PIPELINES' : { 'weblio_word.pipelines.WeblioWordPipeline': 300 }
    }   

    store_cnt = 0
    
    
    def start_requests(self):
        categories = [ 'aa', 'ii', 'uu', 'ee', 'oo',
                       'ka', 'ki', 'ku', 'ke', 'ko',
                       'sa', 'shi', 'su', 'se', 'so',
                       'ta', 'chi', 'tsu', 'te', 'to',
                       'na', 'ni', 'nu', 'ne', 'no',
                       'ha', 'hi', 'hu', 'he', 'ho',
                       'ma', 'mi', 'mu', 'me', 'mo',
                       'ya', 'yu', 'yo',
                       'ra', 'ri', 'ru', 're', 'ro',
                       'wa', 'wo',
                       'ga', 'gi', 'gu', 'ge', 'go',
                       'za', 'zi', 'zu', 'ze', 'zo',
                       'da', 'di', 'de', 'do',
                       'ba', 'bi', 'bu', 'be', 'bo',
                       'pa', 'pi', 'pu', 'pe', 'po' ]
        
        self.basic_url = 'https://kjjk.weblio.jp/category/'
        
        
        for char in categories:
            print(f'character : {char}')
            yield scrapy.Request( url = f'{self.basic_url}{char}', callback = self.find_endpoint)
        

    def find_endpoint(self, response):
        try:
            end_num = int(response.xpath('//div[@class = "CtgryPg"]/span[@class = "CtgryPgNIE"]/a/text()')[-2].extract())
        except IndexError as ierr:
            end_num = 1
        
        for num in range(1, end_num+1):
            yield scrapy.Request(url = f'{response.url}/{num}', callback = self.extract_word_url)
    
    
    def extract_word_url(self, response):
        url_left = response.xpath('//div[@class = "CtgryLink"]/ul[@class = "CtgryUlL"]/li/a/@href').extract()
        url_right = response.xpath('//div[@class = "CtgryLink"]/ul[@class = "CtgryUlR"]/li/a/@href').extract()
        
        for url in url_left+url_right:
            yield scrapy.Request(url = url, callback = self.store_word)
    
    def store_word(self, response):
        self.store_cnt += 1
        
        
        jp_word = response.xpath('//div[@class = "kijiWrp"]//h2[@class = "midashigo"]/text()')[0].extract()
        print(f'{self.store_cnt:>6} : {jp_word}')
        
        kr_word = response.xpath('//div[@class = "kijiWrp"]//span[@lang = "ko"]')[0].xpath('./a/text()').extract()
        if kr_word == []:
            kr_word = response.xpath('//div[@class = "kijiWrp"]//span[@lang = "ko"]')[0].xpath('./text()').extract()
        
        
        # kr_word는 길이가 어느 정도일지 알 수 없음. 일단 1 이상.
        item = WeblioWordItem()
        
        item['jp_word'] = jp_word # str
        item['kr_word'] = kr_word # list
        
        return item