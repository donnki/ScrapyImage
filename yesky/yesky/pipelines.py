# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
}

class MyImagesPipeline(ImagesPipeline):

    #Name download version
    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.url.split('/')[-1]
        # item=request.meta['item']
        title = request.cookies["title"][0].strip().replace("/","_")
        name = request.cookies["from"][0].strip()
        return '%s/%s/%s' % (name,title,image_guid)

    def get_media_requests(self, item, info):
        #yield Request(item['images']) # Adding meta. Dunno how to put it in one line :-)
        if "image_urls" in item:
            for image in item['image_urls']:
                if not image.startswith("http"):
                    t = item['url'][0].split("/")
                    image = t[0] + "//" + t[2] + image 
                if "replace" in item:
                    image = image.replace(item['replace'][0], item['replace'][1])
                # print(image)
                yield scrapy.Request(image, cookies={'title': item['title'], 'from': item['name']})

class MyFilesPipline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.url.split('/')[-1]
        # item=request.meta['item']
        title = request.cookies["title"][0].strip().replace("/","_")
        name = request.cookies["from"][0].strip()
        return '%s/%s/%s' % (name,title,title+".torrent")

    def item_completed(self, results, items, info):
        # print(results)
        return items

    def get_media_requests(self, item, info):
        if "file_urls" in item:
            for _file in item['file_urls']:
                if not _file.startswith("http"):
                    _file = item['url'][0][0:item['url'][0].rfind("/")+1] + _file
                yield scrapy.Request(_file, headers=headers, cookies={'title': item['title'], 'from': item['name']})

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'w+')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n"
        self.file.write(line)
        self.file.flush()
        return item