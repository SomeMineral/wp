# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JapanShortNovelItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    novel_code = scrapy.Field()
    
class JapanLongNovelItem(scrapy.Item):
    subtitle = scrapy.Field()
    text = scrapy.Field()
    novel_code = scrapy.Field()
    list_num = scrapy.Field()
