Scrapy爬图片

目前有两个Spider: beauty、com5442

执行命令：scrapy crawl beauty -a start=1 -a end=50(表示从第1页抓到第50页， 不传start则默认从第一页开图，不传end表示自动爬到最后一页)