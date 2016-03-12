# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YeskyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AlbumItem(scrapy.Item):
	url = scrapy.Field()
	title = scrapy.Field()
	imgCount = scrapy.Field()

class PageItem(scrapy.Item):
	url = scrapy.Field()
	title = scrapy.Field()
	name = scrapy.Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()
	replace = scrapy.Field()