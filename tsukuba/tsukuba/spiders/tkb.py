from json.decoder import JSONDecodeError
import scrapy
from tsukuba.items import TsukubaItem

class TkbSpider(scrapy.Spider):
    name = 'tkb'
    allowed_domains = ['tsukubawebcorpus.jp']
    
    custom_settings = {
    'RANDOMIZE_DOWNLOAD_DELAY': True,
    'DOWNLOAD_DELAY': 0.25, 
    'BOT_NAME': 'kotoba_wo_hirou',
    #'DOWNLOAD_WARNSIZE' : '268,435,456', # 256 MB
    'LOG_LEVEL': 'DEBUG',
    'LOG_FILE' : 'tsukuba.log',  # log 파일 위치
    'ROBOTSTXT_OBEY' : True, 
    'FEED_EXPORT_ENCODING' : 'utf-8',
    'RETRY_ENABLED' : True,
    'RETRY_TIMES': 2,

    'ITEM_PIPELINES' : {'tsukuba.pipelines.TsukubaPipelineAll': 300,

                       },
    'DOWNLOADER_MIDDLEWARES' : {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                                'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
                                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
                                'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
                               },
    }
    
    # 결론 : 빈도..는 예문의 개수와 일치하지 않는다.
    basic_domain = "https://tsukubawebcorpus.jp"
    
    def start_requests(self):
        word_type_dict = {'N' : 57426, 'V' : 33785, 'R' : 115, 'AJ' : 845, 'AN' : 2824, 'AV' : 1864, }
        # 부사(AV) 완료 # na형용사(AN) 완료
        # AJ 1-45 완료
        key = 'AJ'
        start_num = 46
        end_num = 111

        for num in range(start_num, end_num+1):
            pattern_url = f"{self.basic_domain}/patternfreqorder/{key}.{num:0>5}"
            yield scrapy.Request(url=pattern_url, callback=self.id_extractor)

    
    def id_extractor(self, response):
        try:
            word_code = response.url.split('/')[-2] # ex> AV.00001
            rows = response.json()['rows']

        except JSONDecodeError:
            print(f"Error: 내용이 없는 페이지 {response.url}")
            return None
              
        head_col_formdata = {"headword_collocation_id": ' ',
                             "rows": "5000",
                              }
        
        for row in rows:
            head_col_id = f"{word_code}.{row['id']}" # ex> AV.00001.A001
            head_col_url = f"{self.basic_domain}/collocation/{head_col_id}/"
            head_col_formdata['headword_collocation_id'] = head_col_id
            yield scrapy.FormRequest(url=head_col_url, method='POST', formdata=head_col_formdata, callback=self.collocation_record)
    
    
    def collocation_record(self, response):
        record_num = response.json()['records'] # 가장 아래쪽에 record(전체 개수)를 읽어버리자.
        head_col_id = response.url.split('/')[-2] # ex> AV.00001.A001
        
        url_form = f"{self.basic_domain}/example/{head_col_id}"
        example_formdata = {"headword_collocation_id": head_col_id,
                             "rows": "100000",
                            }

        # rows는 0번부터 시작하지만 id, collocation_id는 1부터 시작 ( 정확히는 다섯 자리 수)
        for num in range(1, record_num+1):
            example_url = '{0}.{1:0>5}'.format(url_form,num)
            yield scrapy.FormRequest(url=example_url, method='POST', formdata=example_formdata, callback=self.example_page_total_inspector)


    def example_page_total_inspector(self, response):
        page_total = response.json()['total']
        head_col_id = response.url.split('/')[-2]

        example_url = f"{self.basic_domain}/example/{head_col_id}/"
        
        head_col_formdata = { "headword_collocation_id" : head_col_id,
                                "rows" : "100000",
                                "page" : ' ',
                              }
        # dont_filter = True : 같은 페이지를 또 다시 불러와도 거르지 않기
        for num in range(1, page_total+1):
            head_col_formdata['page'] = f'{num}'
            yield scrapy.FormRequest(url=example_url, method='POST', formdata=head_col_formdata, callback=self.example_extractor, dont_filter=True)


    def example_extractor(self, response):
        item = TsukubaItem()
        item['hcid'] = response.url.split('/')[-2] # 아! 코드 두 자리인 녀석들도 있구나.
        item['json_box'] = response.json()
        return item