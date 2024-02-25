import scrapy
from qidianspider.items import XiaoshuoItem,authorsItem,collectionItem
from scrapy import Selector
class ThebookSpider(scrapy.Spider):
    name = "thebook"
    allowed_domains = ["qidian.com"]
    start_urls = ["https://www.qidian.com/all/orderId11/"]

    url='https://www.qidian.com/all/orderId11-page%d/'
    page=2
    def parse(self, response,**kwargs):
        # #打开本地保存已破译的html
        # return localbook()
        li_list=response.xpath("//*[@id='book-img-text']/ul/li")
        for li in li_list:
            name=li.xpath("./div[2]/h2/a/@href").extract_first()#作者详情地址
            href= li.xpath("./div[2]/p/a[1]/@href").extract_first()#小说详情地址
            yield scrapy.Request(
                url='https:{}'.format(href),
                method='get',
                callback=self.parse_author
                , dont_filter=True
            )

            yield scrapy.Request(
                url='https:{}'.format(name),
                method='get',
                callback=self.parse_book
                , dont_filter=True
            )
            # #全站爬取
            # if self.page <= 10:#获取的页数
            #     # 拼接新的url
            #     new_url = format(self.url%self.page)
            #     self.page += 1
            #     # 手动请求发送。
            #     yield scrapy.Request(url=new_url, callback=self.parse)
            break#仅执行一次

    def parse_book(self,response,**kwargs):
        book_icon='https:'+response.xpath('//*[@id="bookImg"]/img/@src').get()
        name=response.xpath('//*[@id="bookName"]/text()').get()
        author = response.xpath('//div[@class="book-info-top"]//span[1]/text()').extract_first()
        state = response.xpath('//div[@class="book-info-top"]//span[2]/text()').get()
        prop = response.xpath('//div[@class="book-info-top"]//span[6]/text()').get()
        type = response.xpath('//div[@class="book-info-top"]//a[1]/text()').get()
        category = response.xpath('//div[@class="book-info-top"]//a[2]/text()').get()
        word = response.xpath('//div[@class="book-info-top"]//em[1]/text()').get()
        recommend = int(float(response.xpath('//div[@class="book-info-top"]//em[2]/text()').get()[:-1])*10000)
        brief=''.join(response.xpath('//*[@id="book-intro-detail"]/text()').extract())
        print(book_icon,name,author,state,prop,type,category,word,recommend,brief)
        item = XiaoshuoItem()
        item['name'] = name
        item['book_icon'] = book_icon
        item['author'] = author
        item['state'] = False if state=='连载' else True
        item['prop'] =  2 if prop=='VIP' else 1
        item['type'] = type
        item['category'] = category
        item['word'] = word
        item['recommend'] =recommend
        item['brief'] = brief
        yield item




    def parse_author(self, response, **kwargs):
        name = response.xpath("//div[@class='header-msg']/h1/text()").extract_first()
        icon = response.xpath("//div[@class='header-avatar']/img/@src").extract_first()
        introduction = response.xpath("//div[@class='header-msg-desc']/text()").extract_first()
        if not introduction:
            introduction="暂无相关介绍"
        book_total = response.xpath("//div[@class='header-msg-data']/span[1]/strong/text()").extract_first()
        all_word = response.xpath("//div[@class='header-msg-data']/span[2]/strong/text()").extract_first()
        start_work = response.xpath("//div[@class='header-msg-data']/span[3]/strong/text()").extract_first()
        print(name,icon,introduction,book_total,all_word,start_work)
        item = authorsItem()
        item['name']=name
        item['icon']=icon
        item['introduction'] = introduction
        item['book_total'] = book_total
        item['all_word'] =all_word
        item['start_work'] = start_work
        yield item
def localbook():
    body = open(r'C:\Users\l1\Desktop\scrapy_django\okkk.html', encoding='utf-8').read()
    res = Selector(text=body)
    local_list = res.xpath('//*[@id="book-img-text"]/ul/li')
    for li in local_list:
        bookname= li.xpath("./div[2]/h2/a/text()").extract_first()
        coll_num =int(float(li.xpath('./div[2]/p[3]/span/b[2]/span/text()').get())*10000)
        print(bookname, coll_num)
        item=collectionItem()
        item['bookname']=bookname
        item['coll_num']=coll_num
        yield item
