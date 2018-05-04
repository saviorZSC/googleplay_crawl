# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GooglecrawlPipeline(object):
    # print 11111111111
    def process_item(self, item, spider):

        print "11111111"
        # fp = open('F:\PROJECT\googleCrawl\googleCrawl\package_'+item['categories']+'.txt', 'a+')
        # fp.write(item['url'] + '\n')
        return item
from scrapy.exceptions import DropItem

# class DuplicatesPipeline(object):
#
#     def __init__(self):
#         self.ids_seen = set() #注意到set型数据的应用
#
#     def process_item(self, item, spider):
#         if item['id'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['id'])
#             return item
