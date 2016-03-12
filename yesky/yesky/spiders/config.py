
class Config:
	def get(self, key):
		if key == "douban":
			return { 
				'id': 'douban_people',
				'domain': 'douban.com',
				'start_urls': ['https://www.douban.com/people/kiwiit/photos'],
				"xpathAlbumList": '//div[@class="albumlst"]',
				'xpathAlbumURL':'div[@class="albumlst_r"]/div/a/@href',
				'xpathAlbumTitle': 'div[@class="albumlst_r"]/div/a/text()',
				'xpathFirstPage': '//div[@class="photolst clearfix"]/div/a/@href',
				'xpathImagesPath': '//a[@class="mainphoto"]/img/@src',
				'xpathNextImageUrl': '//a[@class="mainphoto"]/@href',
			}
		elif key == "5442":
			return {
				'id': '5442',
				'domain': '5442.com',
				'start_urls': ['http://www.5442.com/tag/rosi.html'],
				"xpathAlbumList": '//div[@class="item_t"]/div',
				'xpathAlbumURL':'a/@href',
				'xpathAlbumTitle': 'a/@title',
				'xpathImagesPath': '//p[@id="contents"]/a/img/@src',
				'xpathNextImageUrl': '//div[@id="aplist"]/ul/li[last()]/a/@href',
			}
		elif key == "yesky":
			return {
				'domain': 'yesky.com',
				'start_urls': ['http://pic.yesky.com/c/6_3655.shtml'],
				"xpathAlbumList": '//div[@class="lb_box"]/dl',
				'xpathAlbumURL':'dd/a/@href',
				'xpathAlbumTitle': 'dd/a/@title',
			}
