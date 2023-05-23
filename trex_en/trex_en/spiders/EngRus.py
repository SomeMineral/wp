from bs4 import BeautifulSoup
import scrapy
from scrapy import Spider, signals

from trex_en.items import EngRusWItem, EngRusSItem
import time


class EngRusSpider(scrapy.Spider):
    
    name = 'EngRus'
    allowed_domains = ['tr-ex.me']
    basic_url = 'https://tr-ex.me'
    language = 'english-russian'
        
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.5,
        'BOT_NAME': 'eng_rus_study',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'eng_rus.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : True,
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'RETRY_TIMES': 10,
    }
    
    
    def start_requests(self):
        basic_queries = f'{self.basic_url}/queries/{self.language}/words/'
        
        start = 0
        end = 10
        for start in range(start, end, 10):  
            range_queries = basic_queries + f'{start}-{end}.html'  
            yield scrapy.Request(url = range_queries, callback = self.word_selector)
    
    def word_selector(self, response):
        words = response.xpath('//div[@class = "item"]/a[@class = "query"]/text()').extract()
        
        frame_url = f'{self.basic_url}/translation/{self.language}/'
        
        for word in words:
            
            yield scrapy.Request(url = frame_url + word, callback = self.word_miner)
    
    # 태그가 복잡하게 섞인 텍스트의 경우, BeautifulSoup이 훨씬 편함. 속도는... 몰라.
    def word_miner(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        
        item_w = EngRusWItem()
        
        item_w['w_Eng'] = soup.find('span', attrs = {'class' : 'query-highlight'}).text
        print(item_w['w_Eng'])
        
        word_translation_tag = soup.find('div', attrs = {'class' : 'query-part'})
        
        if word_translation_tag is None:
            item_w['w_Rus'] = ' '
        else:
            w_Rus_box = []
            for word_tag in word_translation_tag.find_all('a', attrs = {'class' : 'translation'}):
                w_Rus_box.append(word_tag.text)
            item_w['w_Rus'] = w_Rus_box
        
        print(item_w['w_Rus'])
        
        yield item_w
        
        
        # 편의(?)를 위해 그냥 한 번에 ㅠㅠ
        item_s = EngRusSItem()

        for ctx in soup.find_all('div', attrs = {'class' : 'ctx'}):
            s_Eng = ctx.find('div', attrs = {'class' : 'stc stc-s'}).text.strip()
            s_Rus = ctx.find('div', attrs = {'class' : 'stc stc-t'}).text.strip()
            item_s['s_EngRus'] = [s_Eng, s_Rus]
            
            yield item_s
        
        for num in range(1,1000):
            yield scrapy.Request(url = f"https://tr-ex.me/translation/english-russian/{item_w['w_Eng']}?p={num}&page=1&tm=ptable_exact&translation=&target_filter=",
                                 callback = self.added_sentence_finder)
           
              
        
        
    
    
        
    def added_sentence_finder(self, response):
        print('added')      
        for num in range(1,1000):
            
            new_soup = BeautifulSoup(response.text, 'html.parser')
            sentence_list_tag = new_soup.find('div', attrs = {'class':'no-results-filter'})
            
            if sentence_list_tag is None:
                return None
            
            else:
                for ctx in new_soup.find_all('div', attrs = {'class' : 'ctx'}):
                    s_Eng = ctx.find('div', attrs = {'class' : 'stc stc-s'}).text.strip()
                    s_Rus = ctx.find('div', attrs = {'class' : 'stc stc-t'}).text.strip()
                    item_s['s_EngRus'] = [s_Eng, s_Rus]
                    
                    yield item_s
    
    
    
    
    '''
    def find_lowest(self, response):
        
        for large_tag in response.xpath('//div[@class="letters"]'):
            piece = Selector(text = large_tag.extract())
            
            if piece.xpath('h2/a') == 1: # existence of 'a href' -> lower component exist
                url_sub = tag.xpath('h2/a/@href').extract()
                yield scrapy.Request(url = self.basic_url + url_sub, callback = self.find_lowest)

            else:
                words = piece.xpath('//div[@class = "text"]/a/@href').extract()
                for word_href in words:
                    url_word = f'{self.basic_url}{word_href}'
                    yield scrapy.Request(url = url_word, callback = self.word_miner)

    def word_miner(self, response):
        
        item = EngRusItem()
        
        contexts_piece = Selector(text = response.xpath('//div[@id = "contexts" and @class = "block"]')[0].extract())
        doc_piece = Selector(text = response.xpath('//div[@class = "doc-group"]')[0].extract())
        
        item['word_English'] = contexts_piece.xpath('//h2/span/text()')[0].extract()
        #print(f"{item['word_English']}")
        
        
        try:
            word_piece = Selector(text = response.xpath('//div[@id = "query" and @class = "block"]')[0].extract())
            item['word_Russian'] = word_piece.xpath('//span[@class = "text"]/text()').extract() # maybe more than two words

        except IndexError as ie:
            print(f"There is no word in {item['word_English']}")      
            item['word_Russian'] = ''
        
        
        eng_rus_box = list()
        for doc_tag in doc_piece.xpath('//div[@class = "ctx"]'):
            eng_temp = doc_tag.xpath('.//div[@class = "stc stc-s"]//div[@class = "m"]')[0].extract()
            rus_temp = doc_tag.xpath('.//div[@class = "stc stc-t"]//div[@class = "m"]')[0].extract()
            rus_temp_word = doc_tag.xpath('.//div[@class="stc stc-t"]//a[@class = "ctx-link"]/text()')[0].extract()
            eng_rus_box.append([eng_temp, rus_temp, rus_temp_word])
        
        item['doc_EngRus'] = eng_rus_box
        
        return item
    
    '''
        
        
        
