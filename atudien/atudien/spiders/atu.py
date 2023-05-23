import random
import scrapy
import time

from atudien.items import AtudienWordItem, AtudienSentenceItem, AtudienEmptyItem
from urllib.parse import unquote


class AtuSpider(scrapy.Spider):

    name = 'atu'
    allowed_domains = ['atudien.com']
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.25,
        'BOT_NAME': 'kor_study',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'atudien.log',  # log 파일 위치
        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 2,
        'ITEM_PIPELINES': {'atudien.pipelines.AtudienPipeline': 300,
                           },
        'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                                   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
                                   'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
                                   'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
                                   },
    }
    work_type = 'sentence_pair' # 'word_kr', 'sentence_pair'


    def start_requests(self):

        if self.work_type == 'word_kr':
            url_form = 'https://atudien.com/han-viet?page={}'
            for num in range(1,249+1):
                yield scrapy.Request(url=url_form.format(num), callback=self.word_list)

        if self.work_type == 'sentence_pair':
            with open('word_kr.txt', 'r', encoding='utf-8') as words:
                url_form = 'https://atudien.com/han-viet/{}' # 한글 넣어도 알아서 변환해서 접속해줌. 굳
                for idx, word in enumerate(words, start = 1):
                    if idx % 2000 == 0:
                        print('잠시 쉽니다 ({:>5}개 읽음)'.format(idx))
                        time.sleep(random.uniform(10,30))
                    if idx > 4000:
                        print('4000개 끝남.')
                        return None
                    yield scrapy.Request(url=url_form.format(word), callback=self.example_sentence)


    def word_list(self, response):

        # 첫 페이지는 추천 단어 느낌으로 한 칸이 더 있어서 구분해줘야 함.
        item = AtudienWordItem()
        word_box = []

        if response.url[-2:] == '=1':
            target_box = response.xpath('//ul[@class="tag_sml"]')[1]
        else:
            target_box = response.xpath('//ul[@class="tag_sml"]')

        urls = target_box.xpath('.//a/@href').extract()
        for url in urls:
            word_box.append(url.split('/')[-1])

        item['word'] = word_box
        return item


    def example_sentence(self, response):

        target_box = response.xpath('//ul[@class="list_sen"]')
        if target_box == []:
            item = AtudienEmptyItem()
            item['word'] = unquote(response.url.split('/')[-1])
            print('no example : {}'.format(item['word']))
            return item

        item = AtudienSentenceItem()
        box_kr = []
        box_vi = []
        for idx, chunk in enumerate(target_box.xpath('./li')):
            if idx % 2 == 0:
                 box_kr.append(''.join(chunk.xpath('./descendant-or-self::text()').extract()).replace('\n', ''))
            else:
                 box_vi.append(chunk.xpath('./text()')[0].extract().replace('\n',''))

        item['sentence_kr'] = box_kr
        item['sentence_vi'] = box_vi
        print('examples are collected successfully.')
        return item
