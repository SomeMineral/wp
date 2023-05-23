# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TreegalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    number = scrapy.Field()
    title = scrapy.Field()
    main_text = scrapy.Field()
    # comment = scrapy.Field() # 못 읽어... blind 태그 걸려있어서 그런가 ㅠㅠ
    
    