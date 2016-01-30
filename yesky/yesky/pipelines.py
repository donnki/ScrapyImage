# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class MyImagesPipeline(ImagesPipeline):

    #Name download version
    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.url.split('/')[-1]
        # item=request.meta['item']
        title = request.cookies["title"][0].strip()
        return 'full/%s/%s' % (title,image_guid)

    #Name thumbnail version
    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_guid = thumb_id + request.url.split('/')[-1]
        return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

    def get_media_requests(self, item, info):
        #yield Request(item['images']) # Adding meta. Dunno how to put it in one line :-)
        for image in item['image_urls']:
            yield scrapy.Request(image, cookies={'title': item['title']})