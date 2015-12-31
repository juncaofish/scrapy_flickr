#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider
from flickr_crawl.items import PhotoItem
from selenium.webdriver.common.proxy import *
from selenium import webdriver
import sys
import re
import json
import random


reload(sys)
sys.setdefaultencoding('utf-8')


class FlickrSpider(CrawlSpider):

    name = "flickr"
    allowed_domains = ["www.flickr.com", "staticflickr.com", "api.flickr.com"]

    def __init__(self, *args, **kwargs):
        super(FlickrSpider, self).__init__(*args, **kwargs)
        self.emotion = settings.get('TEXT')
        self.js_bin = settings.get('JS_BIN')
        self.api_keys = settings.get('API_KEYS')
        self.url_template = "https://api.flickr.com/services/rest?sort=relevance&parse_tags=1\
        &content_type=7&extras=url_z&per_page=100&page={0}&lang=en-US&text={1}&media=photos&method=flickr.photos.search&api_key={2}&format=json"
        self.start_urls = [
            self.url_template.format(
                1, self.emotion, random.choice(self.api_keys)),
        ]

        service_args = ['--proxy=%s' %
                        settings.get('HTTP_PROXY'), '--proxy-type=http']
        self.driver = webdriver.PhantomJS(
            executable_path=self.js_bin, service_args=service_args)

    def parse(self, response):
        self.driver.get(response.url)
        body = self.driver.page_source
        reg = re.compile(r'jsonFlickrApi\((.*)\)</pre>')
        jdata = json.loads(reg.findall(body)[0])
        pages = jdata.get('photos').get('pages')

        for page in xrange(1, pages):
            yield Request(self.url_template.format(page, self.emotion, random.choice(self.api_keys)), callback=self.parse_download)

    def parse_download(self, response):
        self.driver.get(response.url)
        body = self.driver.page_source
        reg = re.compile(r'jsonFlickrApi\((.*)\)</pre>')
        jdata = json.loads(reg.findall(body)[0])
        photos = jdata.get('photos', None).get('photo', None)
        photos_list = [item.get('url_z', None) for item in photos]

        for url in photos_list:
            if url:
                item = PhotoItem()
                item['emotion'] = self.emotion
                item['image_urls'] = [url]
                item['filename'] = url.split('/')[-1]
                if not item['filename'].lower().endswith('.jpg'):
                    item['filename'] = item['filename'] + '.jpg'
                yield item
