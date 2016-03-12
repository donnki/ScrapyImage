ScrapyImage爬图工具
====
支持配置，修改配置文件config.py，每一项配置如下：
<pre>
{ 
	'id': 'douban_people/fugen',      #ID,将把下载的图片保存到同名目录，支持/子目录
	'domain': 'douban.com',     #域
	'start_urls': ['https://www.douban.com/people/fugen/photos'], #爬图起始地址
	"xpathAlbumList": '//div[@class="albumlst"]',   #相册列表页xpath
	'xpathAlbumURL':'div[@class="albumlst_r"]/div/a/@href',     #相册地址页xpath
	'xpathAlbumTitle': 'div[@class="albumlst_r"]/div/a/text()', #相册标题xpath
	'xpathFirstPage': '//div[@class="photolst clearfix"]/div/a/@href', #第一张图的地址xpath(可以无此字段)
	'xpathImagesPath': '//a[@class="photolst_photo"]/img/@src',,  #图片地址xpath
	'xpathNextImageUrl': '//span[@class="next"]/a/@href',   #图片下一页地址xpath
	'imageUrlReplacement': ['photo/thumb', 'photo/large'],		#缩略图地址替换下就是大图
	'specificAlbums': ['https://www.douban.com/photos/album/128181217/'],  #特殊指定相册，如果有这项，则只下载该相册
}
</pre>
运行方式，执行命令：<br>
scrapy crawl imgspider -a config=douban<br>
<br>
其中：<br>
    -a douban 表示以配置文件config.py里douban对应项下载文件
