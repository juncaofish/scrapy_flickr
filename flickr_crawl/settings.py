# Scrapy settings for flickr_crawl_with_keywords project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'flickr_crawl'

SPIDER_MODULES = ['flickr_crawl.spiders']
NEWSPIDER_MODULE = 'flickr_crawl.spiders'

DOWNLOAD_DELAY = 2.5
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True
HTTP_PROXY = "http://192.168.1.11:8123"
DOWNLOADER_MIDDLEWARES = {
    'flickr_crawl.middlewares.ProxyMiddleware': 100, }

JS_PATTERN = []
JS_BIN = '/usr/local/bin/phantomjs'
JS_WAIT = 2

API_KEYS = ['aa9e1ebb6c132582e697e681196198d8',
            'fd32ca95ae253775a25d6d26225bc55a',
            '892832e49d1bd4ee3d211e723b1e408e',
            'f240b52d4b54626c3e83acdab6c14447',
            '65d8d56fb344ed1234cc2cf5012880f5',
            'e45e88730843f3f69291cff790356bdc',
            '50d4be1f9fc3356be327421a7383b29a']

TEXT = 'angry face'

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {'flickr_crawl.pipelines.FlickrImagePipeline': 100,
                  'flickr_crawl.pipelines.SQLiteStorePipeline': 200}
IMAGES_STORE = './photo/'
IMAGES_EXPIRES = 90
