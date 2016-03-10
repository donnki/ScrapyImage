# -*- coding: utf-8 -*-
import scrapy
from yesky.items import AlbumItem, PageItem
from scrapy.loader import ItemLoader, Identity

class Tuba77Spider(scrapy.Spider):
	name = "tuba77"
	allowed_domains = ["77tuba.com"]

	baseURL = 'http://www.77tuba.com'
	# baseID = "/meinv/list_1_"
	baseID = "/1045/list_1333_"
	suffix = ".shtml"
	
	startPage = None
	endPage = None
	byTag = False

	#scrapy crawl tuba77 -a  -a start=1 -a end=10
	def __init__(self, start=None, end=None, *args, **kwargs):
		super(Tuba77Spider, self).__init__(*args, **kwargs)
		if start != None and start != "1":
			self.start_urls = [self.baseURL + self.baseID + start + self.suffix]
		else:
			self.start_urls = [self.baseURL + self.baseID + "1" + self.suffix]

		if end != None:
			self.endPage = int(end)

	def parse(self, response):
		xpath = '//td[@height="35"]'
		for box in response.xpath(xpath):
			url = self.baseURL + box.xpath('a/@href').extract()[0]
			title = box.xpath('a/text()').extract()[0]
			# print u'', box.xpath('img/@alt').extract()[0]
			# print u'', url, title
			request = scrapy.Request(url, callback=self.parse_first_page, cookies={'title': title})
			yield request
			# break
						
		totalPage = response.xpath('//ul[@class="page"]/text()')[0].re(r'.*?(\d+).*?')[0]
		curPage = response.xpath('//ul[@class="page"]/select/option[@selected]/text()')[0].extract()
		# print u'~~~~', totalPage, curPage, self.endPage
		nextPageIndex = int(curPage) + 1
		if (self.endPage == None or nextPageIndex <= self.endPage) and nextPageIndex <= totalPage: 
			nextUrl = self.baseURL + self.baseID + str(nextPageIndex) + self.suffix
			# print nextUrl
			request = scrapy.Request(nextUrl, callback=self.parse)
			yield request


	def parse_first_page(self, response):
		count = int(response.xpath('//ul[@class="image"]/text()')[0].re(r'.*?(\d+).*?')[0])
		title = response.request.cookies['title']
		albumURL = response.url.replace(".shtml", '')
		# print u'', count, title, albumURL
		for x in xrange(1,count+1):
			suffix = ".shtml"
			if x > 1:
				suffix = "_"+str(x)+".shtml"
				# print u'',albumURL+suffix
				request = scrapy.Request(albumURL+suffix, callback=self.parse_item, cookies={'title': title})
				yield request
				
		l = ItemLoader(item=PageItem(), response=response)
		l.add_value('title', title)
		l.add_value('name', self.name)
		l.add_value('url', response.url)
		l.add_xpath('image_urls', '//td[@valign="top"]/img/@src')
		yield l.load_item()

	def parse_item(self, response):
		l = ItemLoader(item=PageItem(), response=response)
		l.add_value('title', response.request.cookies['title'])
		l.add_value('name', self.name)
		l.add_value('url', response.url)
		l.add_xpath('image_urls', '//td[@valign="top"]/img/@src')
		return l.load_item()
