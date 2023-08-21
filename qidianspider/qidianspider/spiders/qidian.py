import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from lxml import etree

from scrapy import Selector


class QidianSpiderSpider(CrawlSpider):
    name = "qidian"
    allowed_domains = ["www.qidian.com"]
    start_urls = ["https://www.qidian.com/all"]
    #匹配收藏数
    collection_link=LinkExtractor(allow=r"/orderId[1]{2}/")
    # 匹配书籍详情https://www.qidian.com/all
    blocklink = LinkExtractor(allow=r"/book/\d+")
    #匹配书的种类类型
    category_link=LinkExtractor(allow=r"/chanId21/")
    detial_link = LinkExtractor(allow=r"/chanId\d+\-subCateId\d+/")
    #匹配作者信息
    author_link = LinkExtractor(allow=r"Items/")
    booklist_link=LinkExtractor(allow=r"Items/")
    rules = (
        Rule(collection_link, callback="parse_collection",follow=False),
        # Rule(book_link, callback="parseok"),
        # Rule(category_link, callback="parse_type"),
        # Rule(detial_link, callback="parse_ca",follow=True),
        Rule(author_link, callback="parse_item"),
        Rule(booklist_link, callback="parse_item"),
    )
    #
    #
    #
    def parse_collection(self, response):
        # print(response)
        # #打开本地保存已破译的html
        body = open(r'C:\Users\l1\Desktop\scrapy_django\okkk.html', encoding='utf-8').read()
        res = Selector(text=body)
        local_list = res.xpath('//*[@id="book-img-text"]/ul/li')
        for li in local_list:
            name = li.xpath("./div[2]/h2/a/text()").extract_first()
            collection = li.xpath('./div[2]/p[3]/span/b[2]/span/text()').get()
            print(name,collection)
            break

    def parse_book(self, response):
        li_list=response.xpath('//div[@class="work-filter type-filter"]/ul/li/a')
        for li in li_list:

            zz=li.xpath('./text()').get()
            print(zz)
    #
    # def parse_type(self, response):
    #     li_list=response.xpath('//div[@class="work-filter type-filter"]/ul/li/a')
    #     for li in li_list:
    #         # print(li)
    #         zz=li.xpath('./text()').get()
    #         print(zz)
    #
    #     return
    #
    # def parse_ca(self, response):
    #     print(response)
    #
    #     li_list=response.xpath('//div[@class="sub-type"]/dl/dd/a')
    #     for li in li_list:
    #         # print(li)
    #         zz=li.xpath('./text()').get()
    #         print(zz)
    #
    #     return