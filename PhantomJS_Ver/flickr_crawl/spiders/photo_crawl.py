#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from flickr_crawl_with_keywords.items import PhotoItem
from selenium.webdriver.common.proxy import *
import sys
import time
import re
import sqlite3
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')


class FlickrSpider(CrawlSpider):

    name = "flickr"
    allowed_domains = ["www.flickr.com", "staticflickr.com"]

    def __init__(self, emotion='smile face', start='20100101', end='20151221', interval=30, *args, **kwargs):
        super(FlickrSpider, self).__init__(*args, **kwargs)
        self.emotion = emotion
        self.start_date = start
        self.js_bin = settings.get('JS_BIN')
        self.js_wait = settings.get('JS_WAIT')
        start_date = int(time.mktime(time.strptime(start, '%Y%m%d')))
        end_date = int(time.mktime(time.strptime(end, '%Y%m%d')))

        ONEDAYSECONDS = 24 * 3600
        num = (end_date - start_date) // (int(interval) * ONEDAYSECONDS)
        startlist = [(start_date + i * int(interval) * ONEDAYSECONDS, start_date +
                      (i + 1) * int(interval) * ONEDAYSECONDS) for i in xrange(num)]

        self.start_urls = [
            "http://www.flickr.com/search/?text={0}&view_all=1&media=photos&min_upload_date={1}&max_upload_date={2}"
            .format(emotion, *dateInterval) for dateInterval in startlist
        ]

        self.conn = sqlite3.connect('%s%s.db' % (emotion, start))
        self._create_table()
        service_args = ['--proxy=%s' %
                        settings.get('HTTP_PROXY'), '--proxy-type=http', '--load-images=false']

        self.driver = webdriver.PhantomJS(
            executable_path=self.js_bin, service_args=service_args)
        self.driver.set_window_size(1920, 1080)
        self.rules = [
            Rule(LinkExtractor(allow=['search/?text=%s&view_all=1' % emotion]), )]

    def _create_table(self):
        sql1 = '''
        drop table if exists photos;
        '''
        sql2 = '''
        create table if not exists photos (
        photo_id text,
        emotion  text,
        osize_url text,
        download_url text
        );
        '''

        self.conn.execute(sql1)
        self.conn.execute(sql2)
        self.conn.commit()

    def parse(self, response):

        self.driver.get(response.url)
        time.sleep(self.js_wait)
        newHeight = self.driver.execute_script(
            "return document.body.scrollHeight")

        tries = 0
        MAXTRIES = 10
        lastHeight = newHeight = 0
        pageSize = maxSize = 0

        while True:
            try:
                button = self.driver.find_element_by_class_name(
                    "infinite-scroll-load-more")
                button.click()

            except:

                lastHeight = newHeight
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.js_wait)
                newHeight = self.driver.execute_script(
                    "return document.body.scrollHeight")
                pageSize = len(self.driver.page_source)

                if lastHeight == newHeight:
                    tries += 1

                if pageSize > maxSize:
                    maxSize = pageSize
                    maxPage = self.driver.page_source
                    if tries > MAXTRIES:
                        break
                else:
                    break
                print "New height:%s with page size: %s \n" % (newHeight, maxSize)

        # response.replace(body=maxPage)
        reg = re.compile(u'/photos/\w+/\d+/')
        for url in list(set(reg.findall(maxPage))):
            osize_url = 'http://www.flickr.com%ssizes/z/' % url
            photo_id = url.split('/')[-2]
            item = PhotoItem()
            item['emotion'] = self.emotion
            item['osize_url'] = osize_url

            sql = "insert into photos (photo_id, emotion, osize_url) values ('%s', '%s', '%s')" % (
                photo_id, self.emotion, item['osize_url'])

            self.conn.execute(sql)
            self.conn.commit()
            yield Request(url=item['osize_url'], callback=self.parse_download)

    def parse_download(self, response):
        hxs = Selector(response)
        item = PhotoItem()
        photo_id = response.url.split('/')[-4]
        item['image_urls'] = hxs.xpath(
            "//div[@id='allsizes-photo']/img/@src").extract()
        item['photo_id'] = photo_id
        item['emotion'] = self.emotion
        yield item
