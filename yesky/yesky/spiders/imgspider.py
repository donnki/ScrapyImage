# -*- coding: utf-8 -*-
import scrapy
from yesky.items import AlbumItem, PageItem
from scrapy.loader import ItemLoader, Identity
from config import Config

class ImgspiderSpider(scrapy.Spider):
	name = "imgspider"
	allowed_domains = []

	#scrapy crawl imgspider -a config=douban
	def __init__(self, config, *args, **kwargs):
		super(ImgspiderSpider, self).__init__(*args, **kwargs)
		self.config = Config().get(config)
		if self.config != None:
			self.allowed_domains.append(self.config['domain'])
			self.start_urls = self.config['start_urls']
		else:
			print u"配置信息不存在：", config
		
	#爬虫入口，解析相册列表页
	def parse(self, response):
		#获取当前页的每一个相册地址，调用parse_albumm解析相册
		for box in response.xpath(self.config["xpathAlbumList"]):
			url = box.xpath(self.config["xpathAlbumURL"]).extract()[0]
			title = box.xpath(self.config["xpathAlbumTitle"]).extract()[0]
			print u'~~~~~~~~', url, title
			request = scrapy.Request(url, callback=self.parse_album, cookies={'title': title})
			yield request
			break

		#TODO：获取下一页列表页地址，递归调用parse_album_list
		pass

	#解析相册图片列表页
	def parse_album(self, response):
		#获取第一页地址
		if self.config.has_key("xpathFirstPage"):
			firstPage = response.xpath(self.config["xpathFirstPage"]).extract()[0]
			request = scrapy.Request(firstPage, callback=self.parse_page, cookies={'title': response.request.cookies['title']})
			yield request
		else:
			# print u'~~~~~~~~配置中xpathFirstPage不存在，自动将当前页设为相册第一页，开始抓取'
			l = ItemLoader(item=PageItem(), response=response)
			l.add_value('title', response.request.cookies['title'])
			l.add_value('name', self.config["id"])
			l.add_value('url', response.url)
			l.add_xpath('image_urls', self.config["xpathImagesPath"])
			yield l.load_item()
			
			#TODO：获取下一页地址，递归调用自parse_page
			nextPage = response.xpath(self.config["xpathNextImageUrl"]).extract()[0]
			if not nextPage.startswith("http"):
				if nextPage.startswith("/"):
					nextPage = response.url[0:response.url.index("/",10)+1]+nextPage 
				else:
					nextPage = response.url[0:response.url.rfind("/")+1]+nextPage 
			request = scrapy.Request(nextPage, callback=self.parse_page, cookies={'title': response.request.cookies['title']})
			yield request
		

	#解析相册图片展示页
	def parse_page(self, response):
		#爬取图片
		l = ItemLoader(item=PageItem(), response=response)
		l.add_value('title', response.request.cookies['title'])
		l.add_value('name', self.config["id"])
		l.add_value('url', response.url)
		l.add_xpath('image_urls', self.config["xpathImagesPath"])
		yield l.load_item()
		
		#TODO：获取下一页地址，递归调用自parse_page
		nextPage = response.xpath(self.config["xpathNextImageUrl"]).extract()[0]
		if not nextPage.startswith("http"):
			if nextPage.startswith("/"):
				nextPage = response.url[0:response.url.index("/",10)+1]+nextPage 
			else:
				nextPage = response.url[0:response.url.rfind("/")+1]+nextPage 
		request = scrapy.Request(nextPage, callback=self.parse_page, cookies={'title': response.request.cookies['title']})
		yield request
		

