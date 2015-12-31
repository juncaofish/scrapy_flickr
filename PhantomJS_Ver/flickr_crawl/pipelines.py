# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.conf import settings
import os


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
        filename = item['photo_id'] + '.jpg'
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        return '%s/%s' % (item['emotion'], filename)
