# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kpedia.items import KpediaItem, KpediaWordItem

class KpediaPipeline:
    def open_spider(self, spider):
        '''
        self.kpe_kr = open('kpe_kr.txt', 'w', encoding='utf-8')
        self.kpe_jp = open('kpe_jp.txt', 'w', encoding='utf-8')
        '''
        self.kpe_total_word = open('kpe_total_word.txt', 'w', encoding='utf-8')
        self.kpe_kr_word = open('kpe_kr_word.txt', 'w', encoding='utf-8')
        self.kpe_jp_word = open('kpe_jp_word.txt', 'w', encoding='utf-8')
        self.kpe_error_word = open('kpe_error_word.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        '''
        self.kpe_kr.close()
        self.kpe_jp.close()
        '''
        self.kpe_total_word.close()
        self.kpe_kr_word.close()
        self.kpe_jp_word.close()

    def process_item(self, item, spider):
        if isinstance(item, KpediaItem):
            return self.sentence_item(item, spider)

        if isinstance(item, KpediaWordItem):
            return self.word_item(item, spider)

    def sentence_item(self, item, spider):
        for kr_sen, jp_sen in zip(item['kr_sen'],item['jp_sen']):
            self.kpe_kr.write('{}\n'.format(kr_sen))
            self.kpe_jp.write('{}\n'.format(jp_sen))
            print('=====[write]=====\n{0}\n{1}\n================'.format(kr_sen,jp_sen))
        return item

    def word_item(self, item, spider):
        for chunk in item['word']:
            self.kpe_total_word.write('{}\n'.format(chunk))
            try:
                kr_word, jp_word = chunk.split('（') # 으악! 괄호 종류가 다르다니!
                jp_word = jp_word.replace('）', '')
                self.kpe_kr_word.write('{}\n'.format(kr_word))
                self.kpe_jp_word.write('{}\n'.format(jp_word))
                print('=====[write]=====\n{0}\n{1}\n{2}\n================'.format(chunk, kr_word, jp_word))
            except ValueError:
                self.kpe_error_word.write('{}\n'.format(chunk))
                print('====Error====')
                print(chunk)
                print('=============')