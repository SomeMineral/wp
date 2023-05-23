import os
import scrapy
from japan_novel.items import JapanShortNovelItem, JapanLongNovelItem

class NarouSpider(scrapy.Spider):
    name = 'narou'
    allowed_domains = ['syosetu.com']
    
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 2.0, # 이거 좀.. 슬슬 바꿔야하나.. 너무 느리긴 하네.
        'BOT_NAME': 'syosetu_fan',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'narou.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : True, 
        'DEFAULT_REQUEST_HEADERS' : {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0', },
        'FEED_EXPORT_ENCODING' : 'utf-8',
        
        'RETRY_ENABLED' : True,
        'RETRY_TIMES': 2,
        
        'ITEM_PIPELINES' : {'japan_novel.pipelines.JapanNovelPipeline': 300,},
        'DOWNLOADER_MIDDLEWARES' : {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                                    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
                                    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
                                    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
                                   },
    }
    
    long_novel_basic = 'https://ncode.syosetu.com'

    
    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory. ' + directory)

            
    def start_requests(self):
        self.createFolder('novel_box')
        
        novel_code_nums = [101, 102, 201, 202, 301, 302, 303, 304, 305, 306, 307, 401, 402, 403, 404, 9901, 9902, 9903, 9999]
        time_intervals = ['daily', 'weekly', 'monthly', 'quater', 'yearly']
        
        # https://yomou.syosetu.com/rank/genrelist/type/{time_interval}_{novel_code_num}/
        # 1st | div class="ranking_inbox" > div class="ranking_list"
        # 2rd | a href에서 주소 추출
        
        for novel_code_num in novel_code_nums:
            for time_interval in time_intervals:
                rank_list_url = f"https://yomou.syosetu.com/rank/genrelist/type/{time_interval}_{novel_code_num}/"
                yield scrapy.Request( url = rank_list_url, callback = self.rank_list_extractor )

                
    def rank_list_extractor(self, response):
        #print("Here is rank_list_extractor.")
        
        novel_url_list = response.xpath('//div[@class="rank_h"]//a/@href').extract()
        for novel_url in novel_url_list:
            yield scrapy.Request( url = novel_url, callback = self.novel_estimator )

            
    def novel_estimator(self, response):
        #print("Here is novel_estimator.")
        
        # 단편 소설 -> 페이지 그 자체에 텍스트가 담겨있으므로 index 없음!
        if len(response.xpath('//div[@class="index_box"]')) == 0:
            return scrapy.Request(url = response.url, callback = self.novel_extractor, dont_filter = True) # ... dont_filter라니... 
            # 두 번 읽어서 귀찮음.
        else:
            print('장편이라 pass')
            return None
        '''
        # 장편 소설
        novel_sublist_part = response.xpath('//div[@class="index_box"]//dd[@class="subtitle"]/a/@href').extract()
        novel_code = novel_sublist_part[0].split('/')[1]
        novel_title = response.xpath('//p[@class="novel_title"]/text()').extract()[0]
        
        # n으로 시작하는 코드명으로 폴더 만들고, 그 내부에 제목을 담은 'title.txt'파일 생성
        folder_path = f'novel_box/{novel_code}'
        self.createFolder(folder_path)
        
        if not os.path.isfile(f'{folder_path}/title.txt'):     
            with open(f'{folder_path}/title.txt', 'w', encoding = 'utf-8') as t:
                t.write(novel_title)

        for long_novel_part in novel_sublist_part:
            long_novel_url = self.long_novel_basic + long_novel_part
            yield scrapy.Request(url = long_novel_url, callback = self.novel_extractor)
        '''
    
    def novel_extractor(self, response):
        print("Here is novel_extractor.")
        
        # novel_code, list_num
        url_info = response.url.split('/')
        
        # 미리 중복 제거
        if len(url_info) == 6: # 장편
            novel_code = url_info[3]
            list_num = url_info[4]
            if os.path.isfile(f"novel_box/{novel_code}/{list_num:0>4}.txt"):
                print(f"novel_box/{novel_code}/{list_num:0>4}.txt already exists.")
                return None
        
        elif len(url_info) == 5: # 단편
            novel_code = url_info[3]
            if os.path.isfile(f"novel_box/{novel_code}.txt"):
                print(f"novel_box/{novel_code}.txt already exists.")
                return None      
        
        # 본문
        print('본문 점검 시작')
        main_p_tags = response.xpath('//div[@id="novel_honbun"]/p')
        p_box = []
        print('본문 점검 중')
        for p_tag in main_p_tags:
            if len(p_tag.xpath('.//rb')) == 0:
                if len(p_tag.xpath('./text()').extract()) == 0:
                    ruby_not_in = '\n'
                else:
                    ruby_not_in = p_tag.xpath('./text()').extract()[0]
                p_box.append(ruby_not_in)
            else:
                if len(p_tag.xpath('./text() | .//rb/text()')) == 0:
                    ruby_in = '\n'
                else:
                    ruby_in = ''.join(p_tag.xpath('./text() | .//rb/text()').extract())
                p_box.append(ruby_in)
        
        p_box_mod = [ word.replace('\u3000',' ') for word in p_box ]
        print('본문 점검 끝')
        
        
        # 단편/장편에 따라 담을 내용이 좀 다름.
        
        # 단편
        if len(response.xpath('//div[@id="novel_no"]')) == 0:
            item = JapanShortNovelItem()
            item['novel_code'] = url_info[3]
            item['title'] = response.xpath('.//p[@class="novel_title"]/text()')[0].extract()
            item['text'] = p_box_mod
            print(f"spider - {item['novel_code']}")
            return item
        
        # 장편
        else:      
            item = JapanLongNovelItem()
            item['novel_code'] = url_info[3]
            item['list_num'] = url_info[4]
            item['subtitle'] = response.xpath('//p[@class="novel_subtitle"]/text()')[0].extract()
            item['text'] = p_box_mod
            
            print(f"spider - {item['novel_code']}_{item['list_num']:0>4}")
            return item
        
        