# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from atudien.items import AtudienWordItem, AtudienSentenceItem, AtudienEmptyItem

class AtudienPipeline:

    def open_spider(self, spider):

        if spider.work_type == 'word_kr':
            self.word_kr = open('word_kr.txt', 'a', encoding='utf-8')
            self.word_cnt = 0
            print('word_kr.txt open')
        elif spider.work_type == 'sentence_pair':
            self.sentence_kr = open('sentence_kr.txt', 'a', encoding='utf-8')
            self.sentence_vi = open('sentence_vi.txt', 'a', encoding='utf-8')
            self.empty = open('empty.txt', 'a', encoding='utf-8')
            print('sentence_xx.txt open')
        else:
            print('open_spider_error')

    def close_spider(self, spider):
        try:
            if spider.work_type == 'word_kr':
                self.word_kr.close()
            elif spider.work_type == 'sentence_pair':
                self.sentence_kr.close()
                self.sentence_vi.close()
                self.empty.close()
            else:
                print('close_spider_error')
        except (NameError, AttributeError):
            print('except error')

    def process_item(self, item, spider):
        if isinstance(item, AtudienWordItem):
            return self.word_item(item, spider)

        if isinstance(item, AtudienSentenceItem):
            return self.sentence_item(item, spider)

        if isinstance(item, AtudienEmptyItem):
            return self.empty_item(item, spider)


    def word_item(self, item, spider):
        for word in item['word']:
            self.word_kr.write('{}\n'.format(word))
            self.word_cnt += 1
            print('# of words : {0:>4}'.format(self.word_cnt))
        return item


    def sentence_item(self, item, spider):
        # vi : ➥  특수문자 제거
        # kr : \n 개행 제거
        for sen_kr, sen_vi in zip(item['sentence_kr'],item['sentence_vi']):
            sen_kr = sen_kr.strip()
            sen_vi = sen_vi[2:]
            self.sentence_kr.write('{}\n'.format(sen_kr))
            self.sentence_vi.write('{}\n'.format(sen_vi))
        return item


    def empty_item(self, item, spider):
        self.empty.write('{}\n'.format(item['word']))
        return item