# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.conf import settings
import os
import sqlite3


class FlickrImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta=item)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta
        storage = settings.get('IMAGES_STORE')
        subfolder = os.path.join(storage, item['emotion'])
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        return '%s/%s' % (item['emotion'], item['filename'])


class SQLiteStorePipeline(object):

    def __init__(self):
        self.conn = sqlite3.connect('%s.db' % settings.get('TEXT'))
        self.create_table()

    def create_table(self):
        sql1 = '''
        drop table if exists photo;
        '''
        sql2 = '''
        create table if not exists photo (
        name text,
        emotion  text,
        download_url text
        );
        '''

        self.conn.execute(sql1)
        self.conn.execute(sql2)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            sql = "insert into photo (name, emotion, download_url) values ('%s', '%s', '%s')" % (
                item['filename'], item['emotion'], item['image_urls'][0])

            self.conn.execute(sql)
            self.conn.commit()

        except Exception as e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item
