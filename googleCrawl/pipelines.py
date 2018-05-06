# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class GooglecrawlPipeline(object):

	@classmethod
	def from_settings(cls,settings):
		dbparams=dict(
			host=settings['MYSQL_HOST'],
			db=settings['MYSQL_DBNAME'],
			user=settings['MYSQL_USER'],
			passwd=settings['MYSQL_PASSWD'],
			charset='utf8',
			cursorclass=MySQLdb.cursors.DictCursor,
			use_unicode=False,
		)
		dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)
		return cls(dbpool)

	def __init__(self,dbpool):
		self.dbpool = dbpool

	def process_item(self, item, spider):
		query=self.dbpool.runInteraction(self._conditional_insert,item)
		query.addErrback(self._handle_error,item,spider)
		return item


	def _conditional_insert(self,tx,item):
		#print item['name']
		# sql="insert into gplay_app(`url_id`,`update`) values(%s,%s)"
		# params=[item['url'], item['update']]
		# print item['download_num']
		sql="insert into gplay_app(" \
            "`url_id`, `title`, `categories`, `description`, `rating`, `update_date`, `size`, `installs`," \
			"`current_version`, `requires_android`, `content_rating`, `interactive_elements`, `permissions`," \
			"`offered_by`, `developer_web`, `developer_email`, `developer_name`, `privacy_policy`, `update`) " \
			"values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		params=[item["url"], item["title"], item['categories'], item['description'],
				item['rating'], item['update_date'], item['size'], item['download_num'],
				item['cur_version'], item['require'], item['level'], item['interaction'],
				item['authority'], item['developer'], item['dev_web'], item['dev_email'],
				item['dev_name'], item['privacy_policy'],item['update']]
		tx.execute(sql,params)

	def _handle_error(self, failue, item, spider):
		print failue#             return item
