# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglecrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    import scrapy
class GoogleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    categories = scrapy.Field()

    description = scrapy.Field()
    rating = scrapy.Field()

    update_date = scrapy.Field()
    size = scrapy.Field()
    download_num = scrapy.Field()
    cur_version = scrapy.Field()
    require = scrapy.Field()
    level = scrapy.Field()
    interaction = scrapy.Field()
    developer = scrapy.Field()
    dev_web = scrapy.Field()
    dev_email = scrapy.Field()
    dev_name = scrapy.Field()

    authority = scrapy.Field()
    review = scrapy.Field()

    privacy_police = scrapy.Field()


    # dev_url = scrapy.Field()
    # dev_links = scrapy.Field()
    # dev_email = scrapy.Field()
    # dev_web = scrapy.Field()
    # name = scrapy.Field()
    pass
