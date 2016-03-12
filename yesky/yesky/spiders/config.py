
class Config:
	def get(self, key):
		if key == "douban":
			return {
				'domain': 'douban.com',
				'start_urls': ['https://www.douban.com/people/kiwiit/photos'],
				"xpathAlbumList": '//div[@class="albumlst"]',
				'xpathAlbumURL':'div[@class="albumlst_r"]/div/a/@href',
				'xpathAlbumTitle': 'div[@class="albumlst_r"]/div/a/text()',
				'xpathFirstPage': '//div[@class="photolst clearfix"]/div/a/@href',
				'xpathImagesPath': '//a[@class="mainphoto"]/img/@src',
			}
		elif key == "5542":
			return {
				'domain': '5442.com',
				'start_urls': ['http://www.5442.com/tag/rosi/14.html'],
				"xpathAlbumList": '//div[@class="item_t"]/div',
				'xpathAlbumURL':'a/@href',
				'xpathAlbumTitle': 'a/@title',
			}
		elif key == "yesky":
			return {
				'domain': 'yesky.com',
				'start_urls': ['http://pic.yesky.com/c/6_3655.shtml'],
				"xpathAlbumList": '//div[@class="lb_box"]/dl',
				'xpathAlbumURL':'dd/a/@href',
				'xpathAlbumTitle': 'dd/a/@title',
			}
