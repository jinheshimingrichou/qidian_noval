# import scrapy
# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
#
# from scrapy import Selector
# from lxml import etree
#
# # 这里获得所有a标签中的链接
#
# body = open(r'C:\Users\l1\Desktop\scrapy_django\okkk.html', encoding='utf-8').read()
# #使用scrapy自身的Selector解析文本
# res = Selector(text=body)
# li_list = res.xpath('//*[@id="book-img-text"]/ul/li')
#
# for li in li_list:
#     sc = li.xpath('./div[2]/p[3]/span/b[2]/span/text()').extract_first()
#     print(sc,'hh')

# print(li_list)
# 之后可以随意的调戏这个网页了(滑稽脸)
#
# class LocalHtmlSpider(scrapy.Spider):
#     name ="collection_local"
#     start_urls = [
#         'file:///path/to/local/file.html',
#     ]
#
# class CollectionLocalSpider(scrapy.Spider):
#     name ="collection_local"
#     allowed_domains = ["qidian.com"]
#     start_urls = ["https://qidian.com"]
#
#     def parse(self, response,**kwargs):
#         with open(r'C:\Users\l1\Desktop\scrapy_django\okkk.html', encoding='utf-8') as f:
#             res = etree.HTML(f.read())
#             text = etree.tostring(res, encoding='utf-8').decode('utf-8')
#             # 使用scrapy自身的Selector解析文本
#             li_list = res.xpath('//*[@id="book-img-text"]/ul/li[1]/div[2]/p[3]/span/b[2]/span/text()')
#             print(li_list)
