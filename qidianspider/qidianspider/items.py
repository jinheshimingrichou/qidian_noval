# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class XiaoshuoItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    book_icon= scrapy.Field()
    type = scrapy.Field()
    prop = scrapy.Field()
    category = scrapy.Field()
    word = scrapy.Field()
    recommend = scrapy.Field()
    state = scrapy.Field()
    brief = scrapy.Field()
    local_path=scrapy.Field()

class authorsItem(scrapy.Item):
    name = scrapy.Field()
    icon=scrapy.Field()
    introduction = scrapy.Field()
    book_total = scrapy.Field()
    all_word =scrapy.Field()
    start_work=scrapy.Field()
    local_path=scrapy.Field()

class collectionItem(scrapy.Item):
    bookname=scrapy.Field()
    coll_num=scrapy.Field()
