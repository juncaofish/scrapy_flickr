# Scrapy settings for flickr_crawl_with_keywords project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'flickr_crawl_with_keywords'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['flickr_crawl_with_keywords.spiders']
NEWSPIDER_MODULE = 'flickr_crawl_with_keywords.spiders'

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True
HTTP_PROXY = "http://192.168.1.11:8123"
DOWNLOADER_MIDDLEWARES = {
    'flickr_crawl_with_keywords.middlewares.ProxyMiddleware': 100, }

JS_PATTERN = []
JS_BIN = '/usr/local/bin/phantomjs'
JS_WAIT = 2

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'flickr_crawl_with_keywords.pipelines.FlickrImagePipeline': 1}
IMAGES_STORE = './photo/'
IMAGES_EXPIRES = 90
