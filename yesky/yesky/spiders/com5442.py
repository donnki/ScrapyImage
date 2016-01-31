# -*- coding: utf-8 -*-
import scrapy
from yesky.items import AlbumItem, PageItem
from scrapy.loader import ItemLoader, Identity

class Com5442Spider(scrapy.Spider):
	name = "com5442"
	allowed_domains = ["5442.com"]

	baseURL = 'http://www.5442.com'
	baseID = "/meinv/list_1"
	suffix = ".html"
	startPage = None
	endPage = None

	def __init__(self, start=None, end=None, *args, **kwargs):
		super(Com5442Spider, self).__init__(*args, **kwargs)
		if start != None and start != "1":
			self.start_urls = [self.baseURL + self.baseID + "_" + start + self.suffix]
		else:
			self.start_urls = [self.baseURL + self.baseID + "_1" + self.suffix]

		if end != None:
			self.endPage = int(end)

	def parse(self, response):
		for box in response.xpath('//div[@class="imgList"]/ul/li'):
			url = box.xpath('a/@href').extract()[0]
			title = box.xpath('a/@title').extract()[0]
			# print u'', url, title
			request = scrapy.Request(url, callback=self.parse_first_page, cookies={'title': title})
			yield request
			
		nextPageStr = response.xpath('//div[@class="page both"]/ul/li[last()-1]/a/@href')[0].extract()
		nextPageIndex = int(nextPageStr.split(".")[0].split("_")[2])
		if nextPageIndex <= self.endPage:
			nextUrl = self.baseURL + self.baseID + "_" + str(nextPageIndex) + self.suffix
			request = scrapy.Request(nextUrl, callback=self.parse)
			yield request


	def parse_first_page(self, response):
		count = int(response.xpath('//div[@id="aplist"]/ul/li[1]/a/text()')[0].re(r'.*?(\d+).*?')[0])
		title = response.request.cookies['title']
		albumURL = response.url.replace(".html", '')
		for x in xrange(1,count+1):
			suffix = ".html"
			if x > 1:
				suffix = "_"+str(x)+".html"
				request = scrapy.Request(albumURL+suffix, callback=self.parse_item, cookies={'title': title})
				yield request
		l = ItemLoader(item=PageItem(), response=response)
		l.add_value('title', title)
		l.add_value('name', self.name)
		l.add_value('url', response.url)
		l.add_xpath('image_urls', '//p[@id="contents"]/a/img/@src')
		yield l.load_item()

	def parse_item(self, response):
		l = ItemLoader(item=PageItem(), response=response)
		l.add_value('title', response.request.cookies['title'])
		l.add_value('name', self.name)
		l.add_value('url', response.url)
		l.add_xpath('image_urls', '//p[@id="contents"]/a/img/@src')
		return l.load_item()
