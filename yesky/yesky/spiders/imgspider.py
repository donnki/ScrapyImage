# -*- coding: utf-8 -*-
import sys 
import scrapy
from scrapy.http import FormRequest
from yesky.items import AlbumItem, PageItem
from scrapy.loader import ItemLoader, Identity
from config import Config

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class ImgspiderSpider(scrapy.Spider):
	name = "imgspider"
	allowed_domains = []
	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding": "gzip,deflate,sdch",
		"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
		"Connection": "keep-alive",
		"Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
		# "Referer": "http://sexinsex.net/bbs/forum-64-1.html"
	}
	#scrapy crawl imgspider -a config=douban
	def __init__(self, config, *args, **kwargs):
		super(ImgspiderSpider, self).__init__(*args, **kwargs)
		self.config = Config().get(config)
		if self.config != None:
			self.allowed_domains.append(self.config['domain'])
			self.start_urls = self.config['start_urls']
		else:
			print u"配置信息不存在：", config


	def start_requests(self):

		if self.config.has_key("loginFirst"):
			return [scrapy.Request(self.config["loginFirst"]["formURL"], callback = self.parse_login)]  #添加了meta
		else:
			requests = []
			for url in self.start_urls :
				requests.append(scrapy.Request(url, callback=self.parse))
			return requests


	def parse_login(self, response):
		return [FormRequest.from_response(response, 
			headers = self.headers,
			formdata = self.config["loginFirst"]["formdata"],
			callback = self.after_login,
			dont_filter = True
		)]


	def after_login(self, response) :
		# print u'~~~~~~after_login:',("pp3288" in response.body)
		# print(response.headers)
		for url in self.start_urls :
			request = scrapy.Request(url, headers=self.headers, callback=self.parse)
			yield request

	#爬虫入口，解析相册列表页
	def parse(self, response):
		# print response.request.headers
		# print u'~~~~', ("pp3288" in response.body)
		# print u'~~~~', unicode(response.body, "utf8").encode("utf8")
		#获取当前页的每一个相册地址，调用parse_albumm解析相册
		for box in response.xpath(self.config["xpathAlbumList"]):
			url = box.xpath(self.config["xpathAlbumURL"]).extract()[0]
			title = box.xpath(self.config["xpathAlbumTitle"]).extract()[0]
			if not self.config.has_key("specificAlbums") or url in self.config["specificAlbums"]:
				
				if not url.startswith("http") and self.config.has_key("baseAddress"):
					url = self.config["baseAddress"] + url
				print u'加载相册：', title, url
				request = scrapy.Request(url, headers=self.headers, callback=self.parse_album, cookies={'title': title})
				yield request
				# break

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
			# print u'配置中xpathFirstPage不存在，自动将当前页设为相册第一页，开始抓取'
			for x in self.parse_page(response):
				yield x
		

	#解析相册图片展示页
	def parse_page(self, response):
		#爬取图片
		# print u'~~~~', unicode(response.body, "gbk").encode("utf8")
		# print(self.config["xpathImagesPath"])
		# print(response.xpath(self.config["xpathImagesPath"]))
		l = ItemLoader(item=PageItem(), response=response)
		l.add_value('title', response.request.cookies['title'])
		l.add_value('name', self.config["id"])
		l.add_value('url', response.url)
		if self.config.has_key("imageUrlReplacement"):
			l.add_value('replace', self.config["imageUrlReplacement"])
		else:
			l.add_value('replace', False)
		l.add_xpath('image_urls', self.config["xpathImagesPath"])
		yield l.load_item()
		
		#TODO：获取下一页地址，递归调用自parse_page
		if self.config.has_key("xpathNextImageUrl"):
			nextUrls = response.xpath(self.config["xpathNextImageUrl"])
			if len(nextUrls) > 0:
				nextPage = nextUrls.extract()[0]
				if not nextPage.startswith("http"):
					if nextPage.startswith("/"):
						nextPage = response.url[0:response.url.index("/",10)+1]+nextPage 
					else:
						nextPage = response.url[0:response.url.rfind("/")+1]+nextPage 
				request = scrapy.Request(nextPage, callback=self.parse_page, cookies={'title': response.request.cookies['title']})
				yield request
	
	


