import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from lxml import etree

from scrapy import Selector


class QidianSpiderSpider(CrawlSpider):
    name = "qidian_spider"
    allowed_domains = ["www.qidian.com"]
    start_urls = ["https://www.qidian.com"]

    book_link=LinkExtractor(allow=r"/book/\d+/")

    # blocklink = LinkExtractor(allow=r"all/orderId11/")
    category_link=LinkExtractor(allow=r"Items/")
    author_link = LinkExtractor(allow=r"Items/")
    booklist_link=LinkExtractor(allow=r"Items/")
    rules = (
        Rule(book_link, callback="parse_item"),
        # Rule(blocklink, callback="parseok"),
        # Rule(category_link, callback="parse_item", follow=True),
        # Rule(author_link, callback="parse_item", follow=True),
        # Rule(booklist_link, callback="parse_item", follow=True),
    )



    def parse_item(self, response):
        #打开本地保存已破译的html
        body = open(r'C:\Users\l1\Desktop\scrapy_django\okkk.html', encoding='utf-8').read()
        res = Selector(text=body)
        local_list = res.xpath('//*[@id="book-img-text"]/ul/li')
        #获取rule提取链接后相应页面的数据
        li_list=response.xpath("//*[@id='book-img-text']/ul/li")
        for index,li in enumerate(li_list):
            src=li.xpath("./div[@class='book-img-box']/a/img/@src").get()
            name=li.xpath("./div[2]/h2/a/text()").get()
            author =  li.xpath("./div[2]/p/a[1]/text()").get()
            print(src,name,author,)
            # # print(li_list)
            sc = local_list[index].xpath('./div[2]/p[3]/span/b[2]/span/text()').get()
            print(sc)
            # break
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        # return item
    def parseok(self, response, **kwargs):
        pass
        # 使用scrapy自身的Selector解析文本

            # break