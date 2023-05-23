# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
from vnanet.items import VnanetURLItem, VnanetArticleItem

class VnanetPipeline:

    pipe_cnt = 0

    def open_spider(self, spider):
        if spider.purpose == 'url':
            self.vna_pipe = open('url_box_{}.txt'.format(spider.language), 'w', encoding='utf-8')

        if spider.purpose == 'text':
            self.path = './{}_article'.format(spider.language)
            os.makedirs(self.path, exist_ok=True) # 없으면 만들고, 있으면 가만히
            self.error_page = open('error_page_{}.txt'.format(spider.language), 'w', encoding='utf-8')

    def close_spider(self, spider):
        if spider.purpose == 'url':
            self.vna_pipe.close()
        if spider.purpose == 'text':
            self.error_page.close()


    def process_item(self, item, spider):
        if isinstance(item, VnanetURLItem):
            return self.url_writer(item, spider)
        if isinstance(item, VnanetArticleItem):
            return self.article_writer(item, spider)


    def url_writer(self, item, spider):
        # https://vietnam.vnanet.vn/vietnamese/tin-van/
        # https://vietnam.vnanet.vn/vietnamese/long-form/

        for url in item['url']:
            self.vna_pipe.write('{}\n'.format(url))
        return item


    def article_writer(self, item, spider):

        self.pipe_cnt += 1

        with open('{0}/{2:0>5}_{1}.txt'.format(self.path, item['date'], self.pipe_cnt ), 'w', encoding='utf-8') as art:
            art.write('{}\n\n'.format(item['title']))
            temp = (chunk.replace('\n','').replace('\r','').strip() for chunk in item['article'])
            confirmation_text = ' '.join(temp)

            art.write(confirmation_text)
            if len(confirmation_text) < 10:
                self.error_page.write('{}\n'.format(item['title']))

        print('{:0>5}_completed'.format(self.pipe_cnt))
        return item


