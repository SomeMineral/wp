import scrapy
from kpedia.items import KpediaItem, KpediaWordItem

class KpeSpider(scrapy.Spider):
    name = 'kpe'
    allowed_domains = ['www.kpedia.jp']

    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.25,
        'BOT_NAME': 'kotoba_atsume',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'kpedia.log',  # log 파일 위치
        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 2,

        'ITEM_PIPELINES': {'kpedia.pipelines.KpediaPipeline': 300,
                           },
        'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                                   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
                                   'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
                                   'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
                                   },
    }

    def start_requests(self):
        num_tuple = ((1,13),(2,4),(3,6),(4,1),(5,6),(6,8),(7,11),(8,15),(9,15),(12,2),(13,3),(14,6))
        page_form = 'https://www.kpedia.jp/ik/{0}?nCP={1}'
        for first, maximum in num_tuple:
            for second in range(1,maximum+1):
                yield scrapy.Request(url=page_form.format(first,second), callback=self.word_list)

    def word_list(self, response):
        word_list = response.xpath('//div[@id="mainContent"]/table[@align="center"]//a/text()').extract()
        item = KpediaWordItem()
        item['word'] = word_list
        return item

        '''
        sub_urls = response.xpath('//div[@id="mainContent"]/table[@align="center"]//a/@href').extract()
        url_form = "https://www.kpedia.jp{}"
        for sub_url in sub_urls:
            yield scrapy.Request(url=url_form.format(sub_url), callback=self.example_sentence)
        '''

# 단어 수집으로 변경...
'''
    def example_sentence(self,response):
        ex_box = response.xpath('.//table[@style="font-size:14px;line-height:20px;margin-bottom:20px;"]')
        # 예문 없는 경우
        if len(ex_box) == 0:
            print('예문 없음')
            return None

        # kr문장/jp문장 묶음으로 쪼개기 위해 일부러 tr태그 덩어리로 나눔

        kr_sen = []
        jp_sen = []
        for idx, tr_tag in enumerate(ex_box.xpath('.//tr')):
            if tr_tag.xpath('.//a') == []: # 다른 단어의 예문으로 사용되는 경우라서 a태그를 통한 하이퍼링크가 존재.
                if idx % 2 == 0: # 0,2,4, ... -> kr # 문장 첫 구절에 점도 있고 tag로 문장이 쪼개져 있음.
                    split_list = tr_tag.xpath('./td')[1].xpath('./descendant-or-self::text()').extract()
                    kr_sen.append(''.join(split_list))
                else: # 1,3,5, ... ->jp # 한 문장뿐.
                    jp_sen.append(tr_tag.xpath('./td/text()')[0].extract())
            else:
                break

        item = KpediaItem()
        item['kr_sen']=kr_sen
        item['jp_sen']=jp_sen

        return item
'''