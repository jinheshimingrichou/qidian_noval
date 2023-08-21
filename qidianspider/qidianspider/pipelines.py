# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import pymysql
from qidianspider.settings import MYSQL
from qidianspider.items import *


class BookMysqlPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            database=MYSQL['database'],
            user=MYSQL['USER'],
            password=MYSQL['PASSWORD'],
            host=MYSQL['HOST'],
            port=MYSQL['PORT'],
            charset=MYSQL['charset']
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, XiaoshuoItem):
                sql = 'select id from web_authors where web_authors.name=%s'
                self.cursor.execute(sql,item['author'])
                response2 = self.cursor.fetchall()
                item['author']=response2
                # print('res2',response2)
                # print('res1',response1)
                sql = "insert into web_books (name,author,book_icon,type,state,prop,category,word,recommend,brief,collection) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(sql, (item['name'], item['author'], item['local_path'], item['type'],item['state'], item['prop'], item['category'], item['word'],item['recommend'],item['brief'],False))
                print('book收集完成')

            elif isinstance(item, authorsItem):
                sql = "insert into web_authors (name,icon,introduction,book_total,all_word,start_work) values (%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(sql, (item['name'], item['local_path'], item['introduction'], item['book_total'],item['all_word'], item['start_work']))
                print('author收集完成')
            else:
                sql = 'select id from web_books where web_books.name=%s'
                self.cursor.execute(sql, item['bookname'])
                response2 = self.cursor.fetchall()
                item['bookname'] = response2
                sql = "insert into web_collections (coll_num,bookname) values (%s,%s)"
                self.cursor.execute(sql, (item['coll_num'], item['bookname']))
                print('collection收集完成')
            self.conn.commit()
        except Exception as e:
            print(e)
            print(item)
            self.conn.rollback()
        return item


class BookPipeline(ImagesPipeline):  # 继承图片管道
    def get_media_requests(self, item, info):
        if isinstance(item, collectionItem):
            return item
        if isinstance(item, authorsItem):
            yield scrapy.Request(item['icon'],body='author')
        else:
            yield scrapy.Request(item['book_icon'])


    def file_path(self, request, response=None, info=None, *, item=None):
        # print('assssaaaaa',request.body)
        file_name = item['name'] + '.jpg'
        if request.body:
            return f"author/{file_name}"
        return f"book/{file_name}"
    def item_completed(self, results, item, info):
        if isinstance(item, collectionItem):
            return item
        ok, finfo = results[0]
        item['local_path'] = finfo['path']
        # print(item)
        return item
