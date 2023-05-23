# -*- coding: utf-8 -*-

import requests
import scrapy
import urllib

from sedaily.items import SedailyPhotoItem


class SedailyPhotoSpider(scrapy.Spider):
    name = 'sedailyphoto'
    allowed_domains = ['www.sedaily.com',
                       'img.sedaily.com']
    start_urls = ['http://www.sedaily.com/']
    
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 1.0,
        'BOT_NAME': 'plzphoto',
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE' : 'sedailyphoto.log',  # log 파일 위치
        'ROBOTSTXT_OBEY' : True,
        'FEED_EXPORT_ENCODING' : 'utf-8',
        'ITEM_PIPELINES' : {'sedaily.pipelines.SedailyPhotoPipeline': 100},
        'IMAGES_STORE' : 'c:/users/user/desktop/general/sedaily/sedaily_photo',
        'CONCURRENT_REQUESTS' : 10,
        #'HTTPCACHE_ENABLED' : True,
        'ROBOTSTXT_OBEY' : False, # False 설정하면 robots.txt 관련 오류는 안 나오긴 한데...
    }   
    
    def __init__(self):

        self.basic_url = 'https://www.sedaily.com/Photo'
              
        # first
        self.result_basis = '/Gallery/GetGalleryData' # 검색 결과
        self.count_basis = '/Gallery/GetGalleryTotal' # 검색 결과 수
        
        # second
        self.viewer_basis = '/Gallery/Viewer'
        self.viewer_row_basis = '/Gallery/GetGUnit' # viewer 내의 정보
        
        # last
        self.image_basic_url = 'https://img.sedaily.com' # 사진 직접 접근
        
        # params
        self.result_params = {'sType' : '0', # 0 : 최신순, 1: 인기순
                             'gClass' : '', # blank : 전체, E : 연예, S : 스포츠, L : 라이프, P : 정치, C : 경제
                             'sKeyword' : '', # 검색어
                             'page' : '1'
                             }
        self.viewer_params = {'gKey' : '',
                              'rowNums' : '1'
                             }
        
        
    def start_requests(self):
        self.result_params['sKeyword'] = '나른'
        
        count_sub_url = urllib.parse.urlencode(self.result_params)
        
        count_url = self.basic_url + self.count_basis + '?' + count_sub_url
        
        try:
            yield scrapy.Request(url = count_url, callback = self.result_page_analyzer, method = 'POST')
        except:
            print('**********알 수 없는 오류가 발생했습니다.**********')
            return None
        
        
    def result_page_analyzer(self, response):
        
        count_js = response.json() 
        
        try:
            totalcnt = count_js['totalCnt']
            #print(f'{totalcnt=}')
        except Exception as err:
            print(f'전체 결과 개수를 찾을 수가 없습니다.\n{err}')
            return None
        
        if totalcnt == 0: # scrapy에서 response로 찾으니 int로 인식하네.
            print('검색 결과가 없습니다.')
            return None  
        
        # 목록당 20개씩.
        NumOfResultPage = totalcnt // 20
        
        if totalcnt % 20 != 0:
            NumOfResultPage += 1
        
        for result_page_num in range(1, NumOfResultPage + 1):
            self.result_params['page'] = str(result_page_num)
            
            result_page_sub_url = urllib.parse.urlencode(self.result_params)
            result_page_url = self.basic_url + self.result_basis + '?' + result_page_sub_url
                        
            print(f'{result_page_url=}')
            yield scrapy.Request(url = result_page_url, callback = self.viewer_tracer, method = 'POST')
        
        
    def viewer_tracer(self, response):
        
        viewer_trace_js = response.json()
        
        try:
            if viewer_trace_js['dataList'] == []:
                print('**********There is no viewer.\n')
                return None    
        except Exception as err:
            print(f'**********viewer trace error\n {err}')
            return None
        
        viewer_seq_list = ( data['Seq'] for data in viewer_trace_js['dataList']) # generator of int
        
        for view_seq in viewer_seq_list:
            self.viewer_params['gKey'] = str(view_seq)
            viewer_page_url = self.basic_url + self.viewer_basis + '/' + self.viewer_params['gKey']
            print(f'{viewer_page_url=}')
            yield scrapy.Request( url = viewer_page_url, callback = self.viewer_page_analyzer)
    
    def viewer_page_analyzer(self, response):
        NumOfImage = int(response.xpath('//*[@id="gallery_container"]/div/div[2]/p[1]/span/text()')[0].extract().strip(' /'))
        #print(f'{NumOfImage=}')
        for viewer_row_num in range(1, NumOfImage + 1):
            self.viewer_params['rowNums'] = viewer_row_num

            viewer_row_sub_url = urllib.parse.urlencode(self.viewer_params)
            viewer_row_url = self.basic_url + self.viewer_row_basis + '?' + viewer_row_sub_url
            #print(f'{viewer_row_url=}')
            yield scrapy.Request(url = viewer_row_url, callback = self.image_tracer)
    
    def image_tracer(self, response):
        
        image_js = response.json()
        try:
            if image_js['dataList'] == []:
                print('**********There is no image.\n')
                return None
        except Exception as err:
            print(f'**********image trace error\n {err}')
            return None
            
        image_params = ((data['GUDate'], data['GImg']) for data in image_js['dataList'])     
        
        
        item = SedailyPhotoItem()
        item['image_urls'] = [self.image_basic_url + date + img for date, img in image_params]
        
        return item
    
        # 훠어어어얼씬 간결하다!
        
        
        '''
        for date, img in image_params:
            image_url = self.image_basic_url + date + img
            #print(image_url)
            yield scrapy.Request(url = image_url, callback = self.image_extractor)
        '''
    
    '''
    def image_extractor(self, response):
        item = SedailyPhotoItem()

        item['image_urls'] = [response.url] # list로 담아야 하는구나...
        print('**********image_url : {}\n'.format(item['image_urls']))
       
        
        return item
    '''