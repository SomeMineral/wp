import scrapy

from vnanet.items import VnanetURLItem, VnanetArticleItem

class VnaSpider(scrapy.Spider):
    name = 'vna'
    allowed_domains = ['vietnam.vnanet.vn']

    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 0.1,
        'BOT_NAME': 'explorer',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'vnanet.log',  # log 파일 위치
        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 2,

        'ITEM_PIPELINES': {'vnanet.pipelines.VnanetPipeline': 300,

                           },
        'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                                   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
                                   'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
                                   'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
                                   },
    }


    # 라오어 라는 언어가 존재했구나. 라오스와 태국 일부 지역 등에서 쓰이는 언어.. 라고 하네?
    # 크메르어 - 캄보디아어

    # form
    # https://vietnam.vnanet.vn/{lang}/sitemaps/news-{month}-{year}.xml
    # from news-1-2018

    # register_namespace 참고. xml 특히.
    # response.selector.register_namespace('h',"http://www.sitemaps.org/schemas/sitemap/0.9")
    # 앞에는 별명, 뒤에는 이용하고자 하는 xml 문서의 상단에 xmlns 정보를 입력


    purpose = 'text' # 'url', 'text'
    url_form = 'https://vietnam.vnanet.vn/{}/sitemaps/news-{}-{}.xml'
    lang = ['vietnamese', 'korean', 'english', 'chinese', 'french', 'spanish', 'japanese', 'russian', 'lao', 'khmer']
    language = lang[9]

    def start_requests(self):

        if self.purpose == 'url':
            for year in range(2018, 2023+1):
                for month in range(1, 12+1):
                    if year == 2023 and month > 4:
                        return None
                    else:
                        yield scrapy.Request(url=self.url_form.format(self.language, month, year), callback=self.collect_url)

        if self.purpose == 'text':
            with open('url_box_{}.txt'.format(self.language), 'r', encoding='utf-8') as ub:
                for url in ub:
                    if url.strip() == '':
                        continue
                    indicator = url.split('/')[4]

                    if indicator == 'long-form':
                        yield scrapy.Request(url=url, callback=self.long_article)

                    else:
                        yield scrapy.Request(url=url, callback=self.tin_article)


    def collect_url(self, response):
        response.selector.register_namespace('h', "http://www.sitemaps.org/schemas/sitemap/0.9")
        # 선언! 앞으로 'h'로 부를거야.
        urls = response.xpath('//h:loc/text()').extract()
        item = VnanetURLItem()
        item['url'] = urls
        return item


    # /tin-van
    # h1 class="bavn-tt-post" : title
    # div class="bavn-main-post" > article > b or span : main text

    # /long-form
    # div class="bavn-mid-post" > article > h1 : title
    # div class="bavn-mid-post" > article > p (> span) : main text
    # div class="bavn-mid-post" > article > p > strong (> span) : 저자? 필요없음!


    def tin_article(self, response):

        date_temp = response.xpath('//div[@class="bavn-top-post"]//time[@class="bavn-time-news"]/text()')[0].extract()
        day, month, year = date_temp.split('/')
        date = '{0}{1}{2}'.format(year, month, day)

        title = response.xpath('//h1[@class="bavn-tt-post"]/text()')[0].extract()
        # response.xpath('//div[@class="bavn-main-post"]/article[@class="lr-ct"]').xpath('./*[not(self::table)]/text()').extract()
        article_temp1 = response.xpath('//div[@class="bavn-main-post"]/article[@class="lr-ct"]//text()[not(ancestor::table)]').extract()
        article_temp2 = (chunk.replace('\xa0', ' ').replace('\u200b','').strip() for chunk in article_temp1)
        article = [chunk for chunk in article_temp2 if chunk != '']

        item = VnanetArticleItem()
        item['date'] = date
        item['title'] = title
        item['article'] = article
        item['url'] = response.url

        return item


    def long_article(self, response):

        date_temp = response.xpath('//div[@class="bavn-mid-post"]/article/time/text()')[0].extract()
        day, month, year = date_temp.split('/')
        date = '{0}{1}{2}'.format(year, month, day)

        title = response.xpath('//div[@class="bavn-mid-post"]/article/h1/text()')[0].extract()

        article_temp1 = response.xpath('//div[@class="bavn-mid-post"]/article[@class="lr-ct"]//text()[not(ancestor::div/@class="lr-caption") and not(ancestor::h1) and not(ancestor::time)]').extract()
        article_temp2 = (chunk.replace('\xa0', ' ').replace('\u200b','').strip() for chunk in article_temp1)
        article = [chunk for chunk in article_temp2 if chunk != '']

        item = VnanetArticleItem()
        item['date'] = date
        item['title'] = title
        item['article'] = article
        item['url'] = response.url

        return item