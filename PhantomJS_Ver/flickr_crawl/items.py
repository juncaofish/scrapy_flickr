# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class PhotoItem(Item):
    photo_id = Field()
    emotion = Field()
    osize_url = Field()
    image_urls = Field()
