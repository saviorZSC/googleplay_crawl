  # -*- coding: utf-8 -*-
import scrapy
import time
import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from googleCrawl.items import GoogleItem
from selenium import webdriver
from language_linkextractor import LanguageLinkExtractor

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import urlparse
import sys
from pprint import pprint
import linecache

class GoogleSpider(CrawlSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    name = "google"
    allowed_domains = ["play.google.com"]

    # start_urls = (
    #     'http://play.google.com/',
    #     # 'https://play.google.com/store/apps/category/FOOD_AND_DRINK'
    #     'https://play.google.com/store/apps/details?id=com.android.chrome'
    #
    # )
    # rules = [
    #         Rule(LanguageLinkExtractor(allow=("/store/apps/details", )), callback='parse_app',follow=True),
    #     ] #

    def __init__(self):
        # firefox_profile = webdriver.FirefoxProfile()
        # firefox_profile.set_preference("permissions.default.image",2)
        # firefox_profile.set_preference("int1.accept_language", "en-GB")
        # firefox_profile.update_preferences()
        # self.driver = webdriver.Firefox(firefox_profile)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('lang=en-GB')
        prefs = {"profile.managed_default_content_settings.images":2, "int1.accept_language": "en-GB"}
        chrome_options.add_experimental_option('prefs',prefs)
        self.driver = webdriver.Chrome(chrome_options = chrome_options)

    def start_requests(self):
        # file = open("F:\Documents\Project\googleplay_crawl\set\gplay_url.txt", "rb")
        #获取url并且去除“”
        # url = linecache.getline(r'F:\Documents\Project\googleplay_crawl\set\gplay_url.txt',10)
        urls = []
        with open('F:\Documents\Project\googleplay_crawl\set\package_url.txt') as rfile:
            for f in rfile:
                url = 'https://play.google.com/store/apps/details?id='+ f.strip()
                urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_app)


    def parse_app(self, response):
        # 在这里只获取页面的 URL 以及下载数量
        item = GoogleItem()

        url = response.url
        self.driver.get(url)

        url = urlparse.urlparse(url).query.split('&')[0].split('=')[-1]
        #分类
        categories = response.xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div/div[1]/div[1]/span[2]/a/text()').extract()[0]
        #详情
        desc = response.xpath('//*[@id="fcxH9b"]//content/div[1]/text()').extract()
        if len(desc):
            if str(desc[0].encode('utf-8')) == 'Translate':
                desc.pop(0)
        desc = '`'.join(desc)
        #评分
        rating = dict()
        rating['overall'] = response.xpath('//*[@id="fcxH9b"]//div[@class="BHMmbe"]/text()').extract()
        if(len(rating['overall']) > 0):
            rating['overall'] = rating['overall'][0]
        else:
            rating['overall'] = "0"
        ratings = response.xpath('//span[@title]//@title').extract()
        if(len(ratings) > 0):
            rating['five_star'] = ratings[0]
        else:
            rating['five_star'] = "0"
        if(len(ratings) > 1):
            rating['four_star'] = ratings[1]
        else:
            rating['four_star'] = "0"
        if(len(ratings) > 2):
            rating['three_star'] = ratings[2]
        else:
            rating['three_star'] = "0"
        if(len(ratings) > 3):
            rating['two_star'] = ratings[3]
        else:
            rating['two_star'] = "0"
        if(len(ratings) > 4):
            rating['one_star'] = ratings[4]
            rating['one_star'] = "0"
        rating["total_rating"] = response.xpath('//span[@aria-label]/text()').extract()
        if(len(rating['total_rating'])>0):
            rating['total_rating'] = rating['total_rating'][0]
        else:
            rating['total_rating'] = "0"
        # pprint(rating)

        # 获取权限
        permission_set = set()
        while True:
            try:
                next = self.driver.find_element_by_xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"]//a[@jsname="Hly47e"]')
                next.click()
                time.sleep(3)
                next_list = next.find_elements_by_xpath('//div[@class="fnLizd"]//li')
                # print(len(next_list))
                for element in next_list:
                    # print(element.text)
                    permission_set.add(element.text)
                break
            except NoSuchElementException:
                return
        permission = list(permission_set)



        item['url'] = url
        item['title'] = response.xpath('//*[@id="fcxH9b"]//h1[@class="AHFaub"]/span/text()').extract()[0]
        item['categories'] = categories
        # item['download_num'] = response.xpath('//*[@id="fcxH9b"]//span[@class="AYi5wd TBRnV"]//text()').extract()[0]
        item['description'] = desc
        item["rating"]="one_star:"+rating["one_star"]+";"+"two_star:"+rating["two_star"]+";"+"three_star:"+rating["three_star"]+";"+"four_star:"+rating["four_star"]+";"+"five_star:"+rating["five_star"]+";"+"total_rating:"+rating["total_rating"]+";"+"overall:"+rating["overall"]

        item['update_date'] = response.xpath('//div[contains(text(),"Updated")]/..//span/text()').extract()
        if(len(item['update_date']) > 0):
            item['update_date'] = item['update_date'][0]
        else:
            item['update_date'] = ""

        item['size'] = response.xpath('//div[contains(text(),"Size")]/..//span/text()').extract()
        if(len(item['size']) > 0):
            item['size'] = item['size'][0]
        else:
            item['size'] = ""


        item['download_num'] = response.xpath('//div[contains(text(),"Installs")]/..//span/text()').extract()
        if(len(item['download_num']) > 0):
            item['download_num'] = item['download_num'][0]
        else:
            item['download_num'] = ""

        item['cur_version'] = response.xpath('//div[contains(text(),"Current Version")]/..//span/text()').extract()
        if(len(item['cur_version']) > 0):
            item['cur_version'] = item['cur_version'][0]
        else:
            item['cur_version'] = ""

        item['require'] = response.xpath('//div[contains(text(),"Requires Android")]/..//span/text()').extract()
        if(len(item['require']) > 0):
            item['require'] = item['require'][0]
        else:
            item['require'] = ""


        item['level'] = response.xpath('//div[contains(text(),"Content Rating")]/../span//div/text()').extract()
        if(len(item['level']) > 0):
            item['level'] = '`'.join(item['level'])
        else:
            item['level'] = ""


        item['interaction'] = response.xpath('//div[contains(text(),"Interactive Elements")]/..//span/text()').extract()
        if(len(item['interaction']) > 0):
            item['interaction'] = item['interaction'][0]
        else:
            item['interaction'] = ""

        item['developer'] = response.xpath('//div[contains(text(),"Offered By")]/..//span/text()').extract()
        if(len(item['developer']) > 0):
            item['developer'] = item['developer'][0]
        else:
            item['developer'] = ""

        item['iap'] = response.xpath('//div[contains(text(),"In-app Products")]/..//span/text()').extract()
        if(len(item['iap']) > 0):
            item['iap'] = item['iap'][0]
        else:
            item['iap'] = "0"

        item['dev_web'] = response.xpath('//div[contains(text(),"Developer")]/..//a/@href').extract()
        if(len(item['dev_web']) > 0):
            item['dev_web'] = item['dev_web'][0]
        else:
            item['dev_web'] = ""




        item['dev_email'] = response.xpath('//div[contains(text(),"Developer")]/..//a/@href').extract()
        if(len(item['dev_email']) > 2):
            item['dev_email'] = item['dev_email'][1]
        else:
            item['dev_email'] = ""




        item['dev_name'] = response.xpath('//div[contains(text(),"Developer")]/..//div/text()').extract()
        if(len(item['dev_name']) > 0):
            item['dev_name'][0] = ""
            item['dev_name'] = ''.join(item['dev_name'])
        else:
            item['dev_name'] = ""




        item["privacy_policy"] = response.xpath('//div[contains(text(),"Developer")]/..//a[contains(text(),"Privacy Policy")]/@href').extract()
        if(len(item["privacy_policy"]) > 0):
            item["privacy_policy"] = item["privacy_policy"][0]
        else:
            item["privacy_policy"] = ""



        item["authority"]=""
        if len(permission):
            for per in permission:
                item["authority"]=item["authority"]+per+";"

        update = response.xpath('//*[@id="fcxH9b"]//content/text()').extract()
        if len(update):
            if str(update[0].encode('utf-8')) == 'Translate':
                update.pop(0)
        update = '`'.join(update)
        item['update'] = update

        # with open('F:\PROJECT\googleCrawl\googleCrawl\package_FINANCE.txt', 'w+') as f:
        #     f.write(url + '\n')
        yield item






