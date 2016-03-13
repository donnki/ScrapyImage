# -*- coding: utf-8 -*-

class Config:
	def get(self, key):
		if key == "douban":
			return { 		#豆瓣网友相册
				'id': 'douban_people/fugen',
				'domain': 'douban.com',
				'start_urls': ['https://www.douban.com/people/fugen/photos?start=80'],
				"xpathAlbumList": '//div[@class="albumlst"]',
				'xpathAlbumURL':'div[@class="albumlst_r"]/div/a/@href',
				'xpathAlbumTitle': 'div[@class="albumlst_r"]/div/a/text()',
				# 'xpathFirstPage': '//div[@class="photolst clearfix"]/div/a/@href',
				'specificAlbums': ['https://www.douban.com/photos/album/108449647/'],
				'xpathImagesPath': '//a[@class="photolst_photo"]/img/@src',
				'xpathNextImageUrl': '//span[@class="next"]/a/@href',
				'imageUrlReplacement': ['photo/thumb', 'photo/large'],
				# 'loginFirst': {
				# 	'formURL': "https://www.douban.com/accounts/login",
				# 	'formdata' :{
				# 		"source": "None",
				# 		"redir": "https://www.douban.com/doumail/",
				# 		"form_email": "",
				# 		"form_password": "",
				# 		"login": "登录",
				# 	}
				# },
			}
		elif key == "5442":
			return {
				'id': '5442',
				'domain': '5442.com',
				'start_urls': ['http://www.5442.com/tag/rosi/2.html'],
				"xpathAlbumList": '//div[@class="item_t"]/div',
				'xpathAlbumURL':'a/@href',
				'xpathAlbumTitle': 'a/@title',
				'xpathImagesPath': '//p[@id="contents"]/a/img/@src',
				'xpathNextImageUrl': '//div[@id="aplist"]/ul/li[last()]/a/@href',
			}
		elif key == "yesky":
			return {
				'id': 'yesky',
				'domain': 'yesky.com',
				'start_urls': ['http://pic.yesky.com/c/6_3655.shtml'],
				"xpathAlbumList": '//div[@class="lb_box"]/dl',
				'xpathAlbumURL':'dd/a/@href',
				'xpathAlbumTitle': 'dd/a/@title',
				'xpathImagesPath': '//div[@class="l_effect_img_mid"]/a/img/@src',
				'xpathNextImageUrl': '//a[@class="effect_img_right"]/@href',
			}
		
