  # -*- coding: utf-8 -*-
import scrapy
import time
import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from googleCrawl.items import GoogleItem
from language_linkextractor import LanguageLinkExtractor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import urlparse
import sys
from pprint import pprint

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
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("permissions.default.image",2)
        firefox_profile.set_preference("int1.accept_language", "en-GB")
        firefox_profile.update_preferences()
        self.driver = webdriver.Firefox(firefox_profile)


    def start_requests(self):

        yield scrapy.Request(url="https://play.google.com/store/apps/details?id=com.google.android.gm", callback=self.parse_app)


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
        desc = ''.join(desc)
        #评分
        rating = dict()
        rating['overall'] = response.xpath('//*[@id="fcxH9b"]//div[@class="BHMmbe"]/text()').extract()[0]
        rating['five_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][1]/span[@class="UfW5d"]/text()').extract()[0]
        rating['four_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][2]/span[@class="UfW5d"]/text()').extract()[0]
        rating['three_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][3]/span[@class="UfW5d"]/text()').extract()[0]
        rating['two_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][4]/span[@class="UfW5d"]/text()').extract()[0]
        rating['one_star'] = response.xpath('//*[@id="fcxH9b"]//div[@class="mMF0fd"][5]/span[@class="UfW5d"]/text()').extract()[0]
        rating["total_rating"] = response.xpath('//*[@id="fcxH9b"]//span[@class="EymY4b"]/span[2]/text()').extract()[0]
        # pprint(rating)

        #获取权限
        permission_set = set()
        while True:
            try:
                next = self.driver.find_element_by_xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"]//a[@jsname="Hly47e"]')
                next.click()
                time.sleep(3)
                next_list = next.find_elements_by_xpath('//div[@class="fnLizd"]//li')
                print(len(next_list))
                for element in next_list:
                    print(element.text)
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

        item['update_date'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][1]//span/text()').extract()[0]
        item['size'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][2]//span/text()').extract()[0]
        item['download_num'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][3]//span/text()').extract()[0]
        item['cur_version'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][4]//span/text()').extract()[0]
        item['require'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][5]//span/text()').extract()[0]
        item['level'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][6]//span/div/text()').extract()[0]
        item['interaction'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][7]//span/text()').extract()[0]
        item['developer'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][8]//span/text()').extract()[0]
        item['dev_web'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][9]//span/div[1]/a/@href').extract()[0]
        item['dev_email'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][9]//span/div[2]/a/text()').extract()[0]
        item['dev_name'] = response.xpath('//*[@id="fcxH9b"]//div[@class="hAyfc"][9]//span/div/text()').extract()[0]

        item["authority"]=""
        if len(permission):
            for per in permission:
                item["authority"]=item["authority"]+per+";"

        # with open('F:\PROJECT\googleCrawl\googleCrawl\package_FINANCE.txt', 'w+') as f:
        #     f.write(url + '\n')
        yield item


