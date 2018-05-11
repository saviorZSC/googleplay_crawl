# # # file = open("package_FINANCE.txt", "w")
# # # file.write("hello")
# # import urlparse
# # url = "https://play.google.com/store/apps/details?id=gifs.funnygifsforwhatsapp&hl=en"
# # app_name = urlparse.urlparse(url).query.split('&')[0].split('=')[-1]
# # print app_name
# #
# from selenium import webdriver
#
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('lang=en-GB')
# prefs = {"profile.managed_default_content_settings.images":2, "int1.accept_language": "en-GB"}
# chrome_options.add_experimental_option('prefs',prefs)
# driver = webdriver.Chrome(chrome_options = chrome_options)
# driver.get('https://play.google.com/store/apps')
#
#
import MySQLdb
import MySQLdb.cursors

db = MySQLdb.connect("localhost", "root", "", "gplay", charset='utf8' )
cursor = db.cursor()
sql = "select `url_id` from `gplay_app` where  `categories` = 'Food & Drink'"
cursor.execute(sql)
data = cursor.fetchall()

file = open("F:\Documents\Project\googleplay_crawl\set\url_Food_Drink.txt", "a")

for url in data:
    file.write(url[0] + '\n')
