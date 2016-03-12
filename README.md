ScrapyImage爬图工具
====
支持配置，修改配置文件config.py，每一项配置如下：
<pre>
{ 
	'id': 'douban_people',      #ID,将把下载的图片保存到同名目录
	'domain': 'douban.com',     #域
	'start_urls': ['https://www.douban.com/people/kiwiit/photos'], #爬图起始地址
	"xpathAlbumList": '//div[@class="albumlst"]',   #相册列表页xpath
	'xpathAlbumURL':'div[@class="albumlst_r"]/div/a/@href',     #相册地址页xpath
	'xpathAlbumTitle': 'div[@class="albumlst_r"]/div/a/text()', #相册标题xpath
	'xpathFirstPage': '//div[@class="photolst clearfix"]/div/a/@href', #第一张图的地址xpath(可以无此字段)
	'xpathImagesPath': '//a[@class="mainphoto"]/img/@src',  #图片地址xpath
	'xpathNextImageUrl': '//a[@class="mainphoto"]/@href',   #图片下一页地址xpath
}
</pre>
运行方式，执行命令：<br>
scrapy crawl imgspider -a config=douban<br>
<br>
其中：<br>
    -a start表示从第1页抓到第50页， 默认从第一页开始<br>
    -a end表示到第多少页为止，默认表示自动爬到最后一页<br>
