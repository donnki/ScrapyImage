# -*- coding: utf-8 -*-
import scrapy
from yesky.items import AlbumItem, PageItem
from scrapy.loader import ItemLoader, Identity

class BeautySpider(scrapy.Spider):
	name = "beauty"
	allowed_domains = ["yesky.com"]
	start_urls = (
		'http://pic.yesky.com/c/6_20477.shtml',
	)
	baseURL = 'http://pic.yesky.com'

	def parse(self, response):
		#解析当前页的所有相册
		for box in response.xpath('//div[@class="lb_box"]/dl'):
			albumImageCount = box.xpath('dt/span/text()').extract()
			if len(albumImageCount)>0:
				imgCount = int(albumImageCount[0].replace("P",""))			#相册的图片数量
				url = box.xpath('dd/a/@href').extract()[0].replace(".shtml", "")
				title = box.xpath('dd/a/@title').extract()[0]
				print u'', title, imgCount
				for x in xrange(1,imgCount+1):
					suffix = ".shtml"
					if x > 1:
						suffix = "_"+str(x)+".shtml"
					request = scrapy.Request(url+suffix, callback=self.parse_item, cookies={'title': title})
					yield request
		#读取下一页
		selector = response.xpath('//div[@class="flym"]/*')
		last = selector[len(selector)-1].xpath("a")
		if len(last) > 0:
			nextPage = self.baseURL+last[0].xpath("@href").extract()[0]
			request2 = scrapy.Request(nextPage, callback=self.parse)
			yield request2
		


	def parse_item(self, response):
		l = ItemLoader(item=PageItem(), response=response)
		l.add_value('title', response.request.cookies['title'])
		l.add_value('url', response.url)
		l.add_xpath('image_urls', '//div[@class="l_effect_img_mid"]/a/img/@src')
		return l.load_item()


